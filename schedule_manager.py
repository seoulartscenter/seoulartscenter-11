import pymysql
from pymysql.cursors import Cursor



# db 연결하는 함수
def get_db_connection() -> pymysql.Connection:
    """데이터베이스에 연결하고 커넥션 객체를 반환합니다."""
    try:
        # Docker 환경에 맞게 포트를 3307로 설정
        return pymysql.connect(host="localhost", port=3307, user="root", password='1234', database='schedule_db')
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")
        exit(1)

def add_schedule(cursor: Cursor):
    """사용자로부터 입력을 받아 새로운 일정을 데이터베이스에 추가합니다."""
    title = input("제목을 입력하세요: ")
    desc = input("설명을 입력하세요: ")
    start_datetime = input("시작 시간 (YYYY-MM-DD HH:MM:SS): ")
    end_datetime = input("종료 시간 (YYYY-MM-DD HH:MM:SS): ")

    # 기존 코드의 오타(lnto) 및 구문 오류 수정
    sql = """
    INSERT INTO schedules (title, description, start_datetime, end_datetime)
    VALUES (%s, %s, %s, %s)
    """
    try:
        # 기존 코드의 args: 오타 수정
        cursor.execute(sql, args=(title, desc, start_datetime, end_datetime))
        print("✅ 일정이 성공적으로 추가되었습니다.")
    except Exception as e:
        print(f"❗️ 일정 추가 중 오류 발생: {e}")


def get_schedules(cursor: Cursor):
    """데이터베이스에서 모든 일정을 가져와서 보기 좋게 출력합니다."""
    sql = "SELECT id, title, description, start_datetime, end_datetime, completed FROM schedules ORDER BY start_datetime"
    cursor.execute(sql)
    schedules = cursor.fetchall()  # 모든 결과를 한 번에 가져옴

    if not schedules:
        print("\n-- 등록된 일정이 없습니다. --\n")
        return

    print("\n--- 전체 일정 보기 ---")
    for schedule in schedules:
        # 완료 여부를 보기 좋게 표시 (True는 '완료', False는 '미완료')
        status = "✅ 완료" if schedule[5] else "□ 미완료"

        print(f"\n[ID: {schedule[0]}] {schedule[1]} ({status})")
        print(f"  - 설명: {schedule[2]}")
        print(f"  - 시간: {schedule[3]} ~ {schedule[4]}")
    print("---------------------\n")


def complete_schedule(cursor: Cursor):
    """특정 ID의 일정을 완료 처리합니다."""

    sql_select = "SELECT id, title FROM schedules WHERE completed = FALSE ORDER BY id"
    cursor.execute(sql_select)
    schedules = cursor.fetchall()

    if not schedules:
        print("\n-- 완료할 수 있는 일정이 없습니다. --\n")
        return

    print("\n--- 완료할 일정을 선택하세요 ---")
    for schedule in schedules:
        print(f"  [ID: {schedule[0]}] {schedule[1]}")
    print("----------------------------")

    try:
        schedule_id = int(input("완료 처리할 일정의 ID를 입력하세요: "))

        sql_update = "UPDATE schedules SET completed = TRUE WHERE id = %s"

        updated_rows = cursor.execute(sql_update, (schedule_id,))

        if updated_rows > 0:
            print(f"✅ ID {schedule_id}번 일정이 완료 처리되었습니다.")
        else:
            print(f"❗️ ID {schedule_id}번을 찾을 수 없습니다. 다시 확인해주세요.")

    except ValueError:
        print("❗️ 잘못된 입력입니다. ID는 숫자로 입력해주세요.")
    except Exception as e:
        print(f"❗️ 처리 중 오류 발생: {e}")


# 메뉴 나타내기
def show_menu() -> str:
    """사용자에게 메뉴를 보여줍니다."""
    print("\n[ 일정 관리 프로그램 ]")
    print("1. 일정 추가")
    print("2. 일정 보기")
    print("3. 일정 완료 처리")
    print("4. 종료")
    return get_user_choice()

# 선택한 메뉴 입력받는 함수
def get_user_choice() -> str:
    """사용자로부터 메뉴 선택을 입력받습니다."""
    return input("메뉴 선택: ")

def main():
    """프로그램의 메인 로직을 실행합니다."""
    conn = get_db_connection()

    cursor = conn.cursor()

    try:
        while True:
            choice = show_menu()
            if choice == "1":
                add_schedule(cursor)
                conn.commit()  # 데이터 변경 후에는 commit 필수
            elif choice == "2":
                get_schedules(cursor)
            elif choice == "3":
                complete_schedule(cursor)
                conn.commit()
            elif choice == "4":
                print("프로그램을 종료합니다.")
                break
            else:
                print("❗️ 잘못된 선택입니다. 다시 선택해주세요.")

    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
        print("데이터베이스 연결이 종료되었습니다.")

if __name__ == '__main__':
    main()