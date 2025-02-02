def get_paging(data_list) :

    # 페이지 번호 가져오기
    page = 1
    
    # 페이지당 아이템 개수
    items_per_page = 10
    
    # 데이터 리스트에서 해당 페이지에 보여질 아이템 인덱스 계산
    start_idx   = (page - 1) * items_per_page
    end_idx     = start_idx + items_per_page
    items       = [data_list[start_idx:end_idx]]

    # 페이지 번호 리스트 계산
    page_numbers = []
    num_pages = int(len(data_list) / items_per_page) + 1
    for i in range(1, num_pages+1):
        page_numbers.append(i)
    
    #return render_template("index.html", items=items, page_numbers=page_numbers, current_page=page)
    return page_numbers