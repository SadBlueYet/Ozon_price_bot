import asyncio
from pyppeteer import launch

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


# Getting the price by link
async def get_price_url(url):
    try:
        browser = await launch()
        page = await browser.newPage()

        await page.setUserAgent(headers["User-Agent"])
        await page.goto(url)

        await page.waitForSelector(".w8k")
        price_element = await page.querySelector(".w8k")

        price_content = await page.evaluate(
            "(element) => element.textContent", price_element
        )

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        await browser.close()
        try:
            return price_content
        except UnboundLocalError:
            return "Ничего не найдно!"


# Getting links with products
async def get_price_article(article):
    try:
        url = f"https://www.ozon.ru/search/?from_global=true&text={article}"
        browser = await launch()
        page = await browser.newPage()

        await page.setUserAgent(headers["User-Agent"])
        await page.goto(url)

        # searching and waiting for a selector on a page
        selector = "a.k2i.tile-hover-target"

        await page.waitForSelector(selector)

        href_values = await page.evaluate(
            f"""(selector) => {{
            const elements = document.querySelectorAll(selector);
            const hrefs = Array.from(elements).map(element => element.getAttribute('href'));
            return hrefs;
        }}""",
            selector,
        )

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        await browser.close()

        try:
            return href_values

        except UnboundLocalError:
            return False


async def check_choise(user_input):
    if user_input.isdigit():
        links = await get_price_article(user_input)

        if links == False:
            return "Ничего не найдено!"

        link = await check_article(links, user_input)

        return await get_price_url(f"https://www.ozon.ru{link}")

    else:
        return await get_price_url(user_input)


async def check_article(links, article):
    articles = []
    for link in links:
        try:
            browser = await launch()
            page = await browser.newPage()
            await page.setUserAgent(headers["User-Agent"])

            await page.goto(f"https://www.ozon.ru{link}")

            await page.waitForSelector(".jz5.zj5")
            price_element = await page.querySelector(".jz5.zj5")

            price_content = await page.evaluate(
                "(element) => element.textContent", price_element
            )
            articles.append(price_content[12:])

        except Exception:
            pass
        finally:
            await browser.close()
    for i in range(len(articles)):
        if articles[i] == article:
            return links[i]
