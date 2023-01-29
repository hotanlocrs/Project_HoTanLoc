from arcface import ArcFace

def Arc_Face_embed(face):
    face_rec=ArcFace.ArcFace()
    if (len(face)>10):
        return face_rec.calc_emb(face)
    return []