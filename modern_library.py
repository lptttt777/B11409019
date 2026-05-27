import os
import json

class LibraryManager:
    def __init__(self, file_name="library_data.json"):
        self.file_name = file_name
        self.books = []
        self.load_data()

    def load_data(self):
        """載入圖書資料，若檔案不存在則初始化為空清單"""
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
            except json.JSONDecodeError:
                print("資料檔案格式錯誤，初始化為空清單")
                self.books = []
        else:
            self.books = []

    def save_data(self):
        """將圖書資料儲存到 JSON 檔案"""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"儲存資料時發生錯誤: {e}")

    def add_book(self, title, isbn, status):
        """新增書籍，避免重複的 ISBN"""
        if self.is_isbn_exist(isbn):
            print("ISBN 已存在")
            return False
        self.books.append({"title": title, "isbn": isbn, "status": status})
        print("新增成功")
        return True

    def is_isbn_exist(self, isbn):
        """檢查 ISBN 是否已存在"""
        return any(book['isbn'] == isbn for book in self.books)

    def show_books(self):
        """顯示所有書籍"""
        if not self.books:
            print("目前沒有任何書籍")
        for book in self.books:
            print(f"書名: {book['title']}, ISBN: {book['isbn']}, 狀態: {book['status']}")

    def borrow_book(self, isbn):
        """借閱書籍，將狀態更新為 'borrowed'"""
        for book in self.books:
            if book['isbn'] == isbn:
                if book['status'] == "borrowed":
                    print("此書已被借出")
                    return False
                book['status'] = "borrowed"
                print("借閱成功")
                return True
        print("找不到該 ISBN 的書籍")
        return False

    def exit_system(self):
        """儲存資料並退出系統"""
        self.save_data()
        print("系統關閉")

def main():
    library = LibraryManager()
    print("=== 圖書管理系統 v1.0 ===")

    while True:
        try:
            op = input("> ").strip()
            if op == "exit":
                library.exit_system()
                break
            elif op.startswith("add "):
                raw = op[4:].split("/")
                if len(raw) == 3:
                    library.add_book(raw[0], raw[1], raw[2])
                else:
                    print("格式錯誤，正確格式: add 書名/ISBN/狀態")
            elif op == "show":
                library.show_books()
            elif op.startswith("borrow "):
                isbn = op[7:]
                library.borrow_book(isbn)
            else:
                print("未知指令")
        except Exception as e:
            print(f"發生錯誤: {e}")

if __name__ == "__main__":
    main()