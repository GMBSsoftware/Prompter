from Text import Text


class Util:

    # 리스트와 메서드를 넘겨 받아서 리스트들을 메서드에 넣어 실행 시키고 반환
    def repeat(self, list_for_processing, method, **kwargs):
        # 결과로 반환할 리스트
        return_list = []

        # 리스트 내용물이 Text객체인지 검사
        is_Text = False

        # 리스트가 아닌 단일 객체면 리스트화 해서 실행
        if not isinstance(list_for_processing, list):
            list_for_processing = [list_for_processing]

        # 리스트에서 하나씩 꺼내서 메서드 실행.
        while list_for_processing:
            item = list_for_processing.pop(0)
            if isinstance(item, Text):
                text_type = item.get_text_type()
                item = str(item)
                is_Text = True

            # 텍스트 클래스면 다시 텍스트로 생성해줘야하는데
            return_list.extend(method(item, **kwargs))

        return return_list
