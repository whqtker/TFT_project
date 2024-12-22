from pymongo import MongoClient

# db의 collection에 data를 삽입하는 함수
def insert_data(db, collection, data):
    client = MongoClient('localhost', 27017)
    db = client[db]
    collection = db[collection]
    
    try:
        # 삽입 시도
        result = collection.insert_many(data)
        print(f"삽입된 데이터 수: {len(result.inserted_ids)}")
    except Exception as e:
        print(f"데이터 삽입 중 오류 발생: {e}")
        
        # 개별 문서 삽입 시도
        success_count = 0
        for doc in data:
            try:
                collection.insert_one(doc)
                success_count += 1
            except Exception as inner_e:
                print(f"문서 삽입 실패: {inner_e}")
        
        print(f"개별 삽입 성공 건수: {success_count}")

    print(f"데이터 저장 완료: {db}.{collection.name}")

# db의 collection에 있는 모든 json을 가져오는 함수
def get_data(db, collection):
    client = MongoClient('localhost', 27017)
    db = client[db]
    collection = db[collection]
    
    try:
        data = list(collection.find())
        return data
    except Exception as e:
        print(f"데이터 가져오기 중 오류 발생: {e}")
        return []