from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self, filters):
        if filters.get("status") == "new":
            movies = self.dao.get_by_status(int(filters.get("page")))

        elif filters.get("page") is not None and int(filters.get("page")) > 0:
            movies = self.dao.get_by_page(int(filters.get("page")))

        else:
            movies = self.dao.get_all()
        return movies

    def create(self, movie_d):
        return self.dao.create(movie_d)

    def update(self, movie_d):
        self.dao.update(movie_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)
