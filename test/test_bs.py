from bs4 import BeautifulSoup


def test_form_action_extraction():
    html = """
    <form method="post" action="/login.php?act=security_check&to=&hash=ee8a48e15ce3a0e452&api_hash=61928d560e7e0f14db">
        <div class="fi_row">
            <span class="field_prefix">+7</span>
            <input type="text" class="textfield field_inline" name="code" style="width:75px;" />
            <span class="field_prefix">&nbsp;17</span>
        </div>
        <div class="fi_row">
            <input class="button" type="submit" value="Confirm" /><div class="near_btn"><a href="/login?act=do_logout&hash=d4701d26d703b1f6f4&api_hash=61928d560e7e0f14db">Log out</a></div>
        </div>
    </form>
    """

    soup = BeautifulSoup(html, 'lxml')
    assert soup.find('form')[
               'action'] == '/login.php?act=security_check&to=&hash=ee8a48e15ce3a0e452&api_hash=61928d560e7e0f14db'
