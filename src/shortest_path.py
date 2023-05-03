import argparse, json, os, wikipedia
# python3 shortest_path.py --from "Erdős number" --to "The Man Who Loved Only Numbers" -v


def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument("--from", dest="src", required=True, help="заголовок начальной страницы wikipedia", type=str)
    parser.add_argument("--to", dest="dest", required=True, help="заголовок конечной страницы wikipedia", type=str)
    parser.add_argument("--non-directed", dest="non_dir", action='store_true')
    parser.add_argument("-v", dest="v_flag", action="store_true", help="выводит пройденный путь")
    non_dir = True
    v_flag = True
    return parser.parse_args().src, parser.parse_args().dest, \
            non_dir if parser.parse_args().non_dir else False, \
            v_flag if parser.parse_args().v_flag else False


def load_data(src):
    db = []
    try:
        with open((os.getenv('WIKI_FILE', 'wiki.json')), 'r') as file:
            db = json.load(file)
    except:
        raise BaseException("Database not found")
    return db


def prepair_data(db, non_dir, my_db: dict = {}):
    for child in db["members"]:
        try:
            if child["title"] not in my_db[db["title"]]:
                my_db[db["title"]].append(child["title"])
        except KeyError:
            my_db[db["title"]] = [child["title"]]
        if non_dir:
            try:
                if db["title"] not in my_db[child["title"]]:
                    my_db[child["title"]].append(db["title"])
            except KeyError:
                my_db[child["title"]] = [db["title"]]
        if not my_db.get(child["title"]):
            my_db[child["title"]] = []
        my_db = prepair_data(child, non_dir, my_db)
    return my_db


def search_path(src, dest, db, curent_path: list = [], best_path: list = []):
    new_path = curent_path.copy()
    new_path.append(src)
    for child in db[src]:
        if child in new_path:
            continue
        if child == dest:
            new_path.append(child)
            if (len(best_path) == 0) or (len(best_path) > len(new_path)):
                best_path = new_path
            return best_path
        elif (len(best_path) > 0) and (len(new_path) >= len(best_path)):
            return best_path
        else:
            best_path = search_path(child, dest, db, new_path, best_path)
    return best_path


def print_answer(path, isFlagV):
    if len(path) == 0:
        print("Path not found")
        return
    if isFlagV:
        print (*path, sep=' -> ')
    print(len(path))
    
    
def main():
    src, dest, non_dir, v_flag = parsing()
    db = load_data(src)
    db = prepair_data(db[0], non_dir)
    try:
        a = db[src]
        a = db[dest]
    except KeyError:
        print("Path not found")
        return
    path = search_path(src, dest, db)
    print_answer(path, v_flag)


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print(e)
