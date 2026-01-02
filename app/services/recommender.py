# Recommender Service (LightFM stub) → Train a hybrid (content + collaborative filtering) model.(Training is manually triggered for now)
from fastapi import Depends
import numpy as np

try:
    from lightfm import LightFM

    HAS_LIGHTFM = True
except Exception:
    HAS_LIGHTFM = False

from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models import StudentProfile, Property, InteractionEvent

from app.db.session import get_db
from scipy.sparse import coo_matrix
from typing import Tuple, Dict, Any, List
import numpy as np


class RecommenderService:
    def __init__(self):
        # If LightFM is available use it, otherwise operate in "stub" mode
        if HAS_LIGHTFM:
            self.model = LightFM(loss="warp")
        else:
            self.model = None  # stub mode

    async def build_matrices(
        self, session: AsyncSession = Depends(get_db)
    ) -> Tuple[Any, Dict[str, int], Dict[str, int]]:
        s_stmt = select(StudentProfile)
        h_stmt = select(Property)
        i_stmt = select(InteractionEvent)

        s_res = await session.execute(s_stmt)
        h_res = await session.execute(h_stmt)
        i_res = await session.execute(i_stmt)

        students = s_res.scalars().all()
        hostels = h_res.scalars().all()
        interactions = i_res.scalars().all()

        # map by user_id (StudentProfile.user_id) and property id
        student_map = {str(s.user_id): i for i, s in enumerate(students)}
        hostel_map = {str(h.id): j for j, h in enumerate(hostels)}

        rows, cols, data = [], [], []
        for inter in interactions:
            uid = str(inter.user_id)
            pid = str(inter.property_id)
            if uid in student_map and pid in hostel_map:
                rows.append(student_map[uid])
                cols.append(hostel_map[pid])
                data.append(1.0 if inter.event_type in ["save", "apply"] else 0.5)

        mat = coo_matrix((data, (rows, cols)), shape=(len(students), len(hostels)))
        return mat, student_map, hostel_map

    async def train(self, session: AsyncSession = Depends(get_db)) -> bool:
        interaction_matrix, student_map, hostel_map = await self.build_matrices(session)
        if interaction_matrix.nnz > 0:
            if HAS_LIGHTFM and self.model is not None:
                self.model.fit(interaction_matrix, epochs=10, num_threads=2)
                return True
            # stub: pretend we trained
            return True
        return False

    async def recommend(
        self, student_id: str, session: AsyncSession = Depends(get_db), top_n: int = 5
    ) -> List[str]:
        # 1. Try LightFM (Interaction-based) first
        s_stmt = select(StudentProfile)
        h_stmt = select(Property)

        s_res = await session.execute(s_stmt)
        h_res = await session.execute(h_stmt)

        students = s_res.scalars().all()
        hostels = h_res.scalars().all()
        student_map = {str(s.user_id): i for i, s in enumerate(students)}
        hostel_map = {str(h.id): j for j, h in enumerate(hostels)}
        rev_hostel_map = {v: k for k, v in hostel_map.items()}

        if student_id not in student_map:
            # User not found in current DB snapshot, might be very new
            pass
        else:
            if HAS_LIGHTFM and self.model is not None:
                try:
                    scores = self.model.predict(
                        student_map[student_id], np.arange(len(hostels))
                    )
                    top_items = np.argsort(-scores)[:top_n]
                    # return property ids (strings)
                    return [rev_hostel_map[i] for i in top_items]
                except Exception:
                    # Model not fitted or prediction failed; fall back to embedding/popularity
                    pass

        # 2. Fallback to Embedding-based recommendation (Content-based)
        # Fetch student profile with embedding
        stmt = select(StudentProfile).where(StudentProfile.user_id == student_id)
        result = await session.execute(stmt)
        student = result.scalars().first()

        if student and student.embedding_vector:
            # Fetch all properties with their feature embeddings
            h_stmt = select(Property).options(selectinload(Property.features))
            h_res = await session.execute(h_stmt)
            hostels_with_features = h_res.scalars().all()

            scores = []
            for h in hostels_with_features:
                if h.features and h.features.embedding_vector:
                    # Calculate cosine similarity (dot product of normalized vectors)
                    v1 = np.array(student.embedding_vector)
                    v2 = np.array(h.features.embedding_vector)
                    score = float(np.dot(v1, v2))
                    scores.append((str(h.id), score))

            if scores:
                # Sort by score descending
                scores.sort(key=lambda x: x[1], reverse=True)
                return [pid for pid, _ in scores[:top_n]]

        # 3. Fallback to Popularity
        # Stub fallback: use simple popularity of properties from recent interactions
        i_stmt = select(InteractionEvent)
        i_res = await session.execute(i_stmt)
        interactions = i_res.scalars().all()
        counts: Dict[str, int] = {}
        for inter in interactions:
            pid = str(inter.property_id)
            counts[pid] = counts.get(pid, 0) + 1

        # sort property ids by popularity
        popular = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        popular_ids = [pid for pid, _ in popular]
        # if not enough popular items, pad with available hostels
        result = popular_ids[:top_n]
        if len(result) < top_n:
            for h in hostels:
                hid = str(h.id)
                if hid not in result:
                    result.append(hid)
                    if len(result) >= top_n:
                        break
        return result
