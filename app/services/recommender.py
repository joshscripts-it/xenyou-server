# Recommender Service (LightFM stub) → Train a hybrid (content + collaborative filtering) model.(Training is manually triggered for now)
from fastapi import Depends
import numpy as np
from lightfm import LightFM
from sqlmodel import Session, select
from app.models import Student, Hostel, Interaction

from app.db.session import get_db
from scipy.sparse import coo_matrix


class RecommenderService:
    def __init__(self):
        self.model = LightFM(loss="warp")

    async def build_matrices(self, session: Session = Depends(get_db)):
        s_stmt = select(Student)
        h_stmt = select(Hostel)
        i_stmt = select(Interaction)

        students = session.exec(s_stmt).all()
        hostels = session.exec(h_stmt).all()
        interactions = session.exec(i_stmt).all()

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

    async def train(self, session: Session = Depends(get_db)):
        interaction_matrix, student_map, hostel_map = self.build_matrices(session)
        if interaction_matrix.nnz > 0:
            self.model.fit(interaction_matrix, epochs=10, num_threads=2)
            return True
        return False

    def recommend(
        self, student_id: int, session: Session = Depends(get_db), top_n: int = 5
    ):
        s_stmt = select(Student)
        h_stmt = select(Hostel)

        students = session.exec(s_stmt).all()
        hostels = session.exec(h_stmt).all()
        student_map = {s.id: i for i, s in enumerate(students)}
        hostel_map = {h.id: j for j, h in enumerate(hostels)}
        rev_hostel_map = {v: k for k, v in hostel_map.items()}

        if student_id not in student_map:
            return []

        scores = self.model.predict(student_map[student_id], np.arange(len(hostels)))
        top_items = np.argsort(-scores)[:top_n]
        return [rev_hostel_map[i] for i in top_items]
