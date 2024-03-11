class Util:
    # 리스트와 메서드를 넘겨 받아서 리스트들을 메서드로 실행 시키고 반환
    def repeat(self, list_for_processing, method):
        # 리스트가 아닌 단일 객체면 리스트화 해서 실행
        if not isinstance(list_for_processing, list):
            list_for_processing = [list_for_processing]
