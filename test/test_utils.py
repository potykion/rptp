from rptp.common.utils import truncate_left, truncate_right


# )

def test_truncate_left():
    assert truncate_left(
        'Ariel.temple Milf mature Ass Babes Няшка Русское домашние Порно anal fuck блондиночка сосёт Эротика Секс в попу Молоденькие br') == \
           'Ariel.temple Milf mature Ass Babes Няшка Русское'

    # todo "viv.16.05.11.lena.love.and.violette.pink.sophisticated" => "viv.16.05.11.lena.love.and.violette"


def test_truncate_right():
    assert truncate_right(
        'Ariel.temple Milf mature Ass Babes Няшка Русское домашние Порно anal fuck блондиночка сосёт Эротика Секс в попу Молоденькие br') == \
           'домашние Порно anal fuck блондиночка сосёт Эротика Секс в попу Молоденькие br'

    assert truncate_right('op op', len_=2) == 'op'

    assert truncate_right('Ariel Temple aka Katarina Muti') == ''
