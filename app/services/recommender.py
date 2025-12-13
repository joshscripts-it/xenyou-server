from typing import List, Optional
import numpy as np
from sqlmodel import select
from app.models.entities import Hostel, Interaction
from app.services.embeddings import get_embedding
from sqlmodel import Session
from lightfm import LightFM
from app.models.models import Student
from scipy.sparse import coo_matrix


def _cosine(a: List[float], b: List[float]) -> float:
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    if a.size == 0 or b.size == 0:
        return 0.0
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def rank_hostels(
    db: Session,
    query: Optional[str] = None,
    budget_max: Optional[float] = None,
    amenities: Optional[List[str]] = None,
    student_id=None,
    top_k: int = 10,
):
    stmt = select(Hostel)
    if budget_max is not None:
        stmt = stmt.where(Hostel.price <= budget_max)
    hostels = db.exec(stmt).all()

    q_emb = None
    if query:
        try:
            q_emb = get_embedding(query)
        except RuntimeError:
            q_emb = None

    # compute base score: semantic similarity if embed available else 0
    scored = []
    # popularity: count of interactions per hostel
    interactions = db.exec(select(Interaction)).all()
    pop_map = {}
    for it in interactions:
        pop_map.setdefault(str(it.hostel_id), 0)
        pop_map[str(it.hostel_id)] += 1

    for h in hostels:
        score = 0.0
        if q_emb and h.embedding:
            try:
                score = _cosine(q_emb, h.embedding)
            except Exception:
                score = 0.0

        # amenity match boost
        if amenities and h.amenities:
            intersection = set(amenities).intersection(set(h.amenities))
            if intersection:
                score += 0.05 * len(intersection)

        # popularity boost (simple collaborative signal)
        score += 0.01 * pop_map.get(str(h.id), 0)

        scored.append((score, h))

    scored.sort(key=lambda x: x[0], reverse=True)
    results = [h for _, h in scored[:top_k]]
    return results


# Recommender Service (LightFM stub) → Train a hybrid (content + collaborative filtering) model.(Training is manually triggered for now)
class RecommenderService:
    def __init__(self):
        self.model = LightFM(loss="warp")

    def build_matrices(self, session: Session):
        students = session.exec(select(Student)).all()
        hostels = session.exec(select(Hostel)).all()
        interactions = session.exec(select(Interaction)).all()

        student_map = {s.id: i for i, s in enumerate(students)}
        hostel_map = {h.id: j for j, h in enumerate(hostels)}

        rows, cols, data = [], [], []
        for inter in interactions:
            if inter.student_id in student_map and inter.hostel_id in hostel_map:
                rows.append(student_map[inter.student_id])
                cols.append(hostel_map[inter.hostel_id])
                data.append(1.0 if inter.action in ["save", "apply"] else 0.5)

        mat = coo_matrix((data, (rows, cols)), shape=(len(students), len(hostels)))
        return mat, student_map, hostel_map

    def train(self, session: Session):
        interaction_matrix, student_map, hostel_map = self.build_matrices(session)
        if interaction_matrix.nnz > 0:
            self.model.fit(interaction_matrix, epochs=10, num_threads=2)
            return True
        return False

    def recommend(self, student_id: int, session: Session, top_n: int = 5):
        students = session.exec(select(Student)).all()
        hostels = session.exec(select(Hostel)).all()
        student_map = {s.id: i for i, s in enumerate(students)}
        hostel_map = {h.id: j for j, h in enumerate(hostels)}
        rev_hostel_map = {v: k for k, v in hostel_map.items()}

        if student_id not in student_map:
            return []

        scores = self.model.predict(student_map[student_id], np.arange(len(hostels)))
        top_items = np.argsort(-scores)[:top_n]
        return [rev_hostel_map[i] for i in top_items]
