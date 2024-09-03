import pytest
from main import BooksCollector


class TestBooksCollector:
    @pytest.mark.parametrize("book_name, expected_result", [
        ("Автостопом по галактике", True),
        ("", False),
        ("a" * 41, False),
        ("Хроники странствующего кота", True)
    ])
    def test_add_new_book(self, book_name, expected_result):
        collector = BooksCollector()
        collector.add_new_book(book_name)

        assert (book_name in collector.get_books_genre()) == expected_result

    def test_add_existing_book(self):
        collector = BooksCollector()
        collector.add_new_book("Консервный ряд")
        length = len(collector.get_books_genre())
        collector.add_new_book("Консервный ряд")
        assert len(collector.get_books_genre()) == length


class TestBooksCollectorSetBookGenre:
    @pytest.mark.parametrize("book_name, genre, expected_genre", [
        ("Автостопом по галактике", "Фантастика", "Фантастика"),
        ("Убийство в Восточном экспрессе", "Детективы", "Детективы"),
    ])
    def test_set_book_genre(self, book_name, genre, expected_genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == expected_genre

    def test_set_genre_for_nonexistent_book(self):
        collector = BooksCollector()
        collector.set_book_genre("Хроники странствующего кота", "Фантастика")
        assert collector.get_book_genre("Хроники странствующего кота") is None

    def test_set_invalid_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Консервный ряд")
        collector.set_book_genre("Консервный ряд", "Драма")
        assert collector.get_book_genre("Консервный ряд") == ""


class TestBooksCollectorGetBookGenre:
    def test_get_genre_for_existing_book_with_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Автостопом по галактике")
        collector.set_book_genre("Автостопом по галактике", "Фантастика")

        assert collector.get_book_genre("Автостопом по галактике") == "Фантастика"

    def test_get_genre_for_existing_book_without_genre(self):
        collector = BooksCollector()
        collector.add_new_book("Консервный ряд")

        assert collector.get_book_genre("Консервный ряд") == ""

    def test_get_genre_for_nonexistent_book(self):
        collector = BooksCollector()

        assert collector.get_book_genre("Хроники странствующего кота") is None


class TestBooksCollectorGetBooksWithSpecificGenre:
    @pytest.mark.parametrize("books, genre, expected_books", [
        ([
             ("Автостопом по галактике", "Фантастика"),
             ("Убийство в Восточном экспрессе", "Детективы")
         ], "Фантастика", ["Автостопом по галактике"]),

        ([], "Фантастика", []),

        ([
             ("Автостопом по галактике", "Фантастика")
         ], "Драма", []),
    ])
    def test_get_books_with_specific_genre(self, books, genre, expected_books):
        collector = BooksCollector()

        for book_name, book_genre in books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, book_genre)

        result = collector.get_books_with_specific_genre(genre)

        assert sorted(result) == sorted(expected_books)


class TestBooksCollectorGetBooksGenre:
    collector = BooksCollector()
    assert collector.get_books_genre() == {}

    collector = BooksCollector()
    collector.add_new_book("Автостопом по галактике")

    assert collector.get_books_genre() == {"Автостопом по галактике": ""}

    collector = BooksCollector()
    collector.add_new_book("Автостопом по галактике")
    collector.add_new_book("Убийство в Восточном экспрессе")
    collector.set_book_genre("Автостопом по галактике", "Фантастика")
    collector.set_book_genre("Убийство в Восточном экспрессе", "Детективы")

    expected_result = {
        "Автостопом по галактике": "Фантастика",
        "Убийство в Восточном экспрессе": "Детективы"
    }

    assert collector.get_books_genre() == expected_result


class TestBooksCollectorGetBooksForChildren:
    @pytest.mark.parametrize("books, expected_books", [
        ([
            ("Автостопом по галактике", "Фантастика"),
            ("Маска", "Комедии"),
            ("Консервный ряд", "Драма"),
        ], ["Автостопом по галактике", "Маска"]),

        ([], []),

        ([
            ("Убийство в Восточном экспрессе", "Детективы"),
            ("Лангольеры", "Ужасы")
        ], []),

        ([
            ("Убийство в Восточном экспрессе", "Детективы"),
            ("Гадкий я", "Мультфильмы")
        ], ["Гадкий я"]),
    ])
    def test_get_books_for_children(self, books, expected_books):
        collector = BooksCollector()

        for book_name, book_genre in books:
            collector.add_new_book(book_name)
            collector.set_book_genre(book_name, book_genre)

        result = collector.get_books_for_children()

        assert sorted(result) == sorted(expected_books)


class TestBooksCollectorAddBookInFavorites:
    @pytest.mark.parametrize("book_name, initial_books, expected_result", [
        ("Автостопом по галактике", ["Автостопом по галактике"], ["Автостопом по галактике"]),
        ("Автостопом по галактике", [], []),
        ("Приключения Электроника", [], [])
    ])
    def test_add_book_in_favorites(self, book_name, initial_books, expected_result):
        collector = BooksCollector()

        for book in initial_books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)

        collector.add_book_in_favorites(book_name)
        result = collector.get_list_of_favorites_books()

        assert sorted(result) == sorted(expected_result)


class TestBooksCollectorDeleteBookFromFavorites:
    @pytest.mark.parametrize("initial_books, book_to_delete, expected_result", [
        (["Автостопом по галактике"], "Автостопом по галактике", []),
        (["Автостопом по галактике", "Убийство в Восточном экспрессе"], "Автостопом по галактике",
         ["Убийство в Восточном экспрессе"]),
        (["Автостопом по галактике"], "Убийство в Восточном экспрессе", ["Автостопом по галактике"]),
        (["Убийство в Восточном экспрессе"], "Приключения Электроника", ["Убийство в Восточном экспрессе"])
    ])
    def test_delete_book_from_favorites(self, initial_books, book_to_delete, expected_result):
        collector = BooksCollector()

        for book in initial_books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)

        collector.delete_book_from_favorites(book_to_delete)
        result = collector.get_list_of_favorites_books()

        assert sorted(result) == sorted(expected_result)


class TestBooksCollectorGetListOfFavoritesBooks:
    @pytest.mark.parametrize("initial_books, deletions, expected_result", [
        ([], [], []),
        (["Автостопом по галактике"], [], ["Автостопом по галактике"]),
        (["Автостопом по галактике", "Убийство в Восточном экспрессе"], [],
         ["Автостопом по галактике", "Убийство в Восточном экспрессе"]),
        (["Автостопом по галактике", "Убийство в Восточном экспрессе"], ["Автостопом по галактике"],
         ["Убийство в Восточном экспрессе"]),
        (["Автостопом по галактике", "Убийство в Восточном экспрессе"],
         ["Автостопом по галактике", "Убийство в Восточном экспрессе"], [])
    ])
    def test_get_list_of_favorites_books(self, initial_books, deletions, expected_result):
        collector = BooksCollector()

        for book in initial_books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)

        for book in deletions:
            collector.delete_book_from_favorites(book)

        result = collector.get_list_of_favorites_books()

        assert sorted(result) == sorted(expected_result)
