from Text import Text


class Util:

    # 리스트와 메서드를 넘겨 받아서 리스트들을 메서드에 넣어 실행 시키고 반환
    def repeat(self, list_for_processing, method, **kwargs):
        # 결과로 반환할 리스트
        return_list = []

        # 메서드 실행 후 반환받은 리스트
        result_list = []

        # Text형일 경우 타입 저장 리스트
        text_type_list = []

        # 리스트 내용물이 Text객체인지 검사
        is_Text = False

        # 전달받은게 리스트가 아닌 단일 객체면 리스트화 해서 실행
        if not isinstance(list_for_processing, list):
            list_for_processing = [list_for_processing]

        # 리스트에서 하나씩 꺼내서 메서드 실행.
        for item in list_for_processing:

            # Text형 이면
            if isinstance(item, Text):
                text_type = item.get_text_type()
                item = str(item)
                is_Text = True

                # 메서드 실행
                result = method(item, **kwargs, text_type=text_type)
            else:
                result = method(item, **kwargs)

            # 메서드 실행 후 리스트가 아니면 리스트화
            if not isinstance(result, list):
                result = [result]

            # 반환된 개수 만큼 Text클래스의 text_type 추가
            text_type_list.extend([text_type] * len(result))

            # 메서드 실행 결과 리스트에 추가
            result_list.extend(result)

        # 전달 받을 때 Text 형이었으면 Text로 생성 후 반환
        if is_Text:
            for return_item, text_type in zip(result_list, text_type_list):
                return_list.append(Text(return_item, text_type))
        else:
            return_list.extend(result_list)

        return return_list
