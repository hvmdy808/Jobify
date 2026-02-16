import csv

class CSV:
    def save(self, data: list[dict], filename: str):

        if not data:
            return

        path = f'D:\\Projects\\PycharmProjects\\Jobify\\data\\{filename}.csv'

        with open(path, "w", newline="", encoding="utf-8") as f:

            writer = csv.DictWriter(f, fieldnames=data[0].keys())

            writer.writeheader()
            writer.writerows(data)
            print(f'Successfully saved to {filename}.csv')