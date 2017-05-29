# NOTE python 3.5+ required
# serve scraper_api.py on locahost:9000

from aiohttp import ClientSession, web
import asyncio
import async_timeout

HOTELS = ["expedia", "orbitz", "hilton", "priceline", "travelocity"]
URL = "http://localhost:9000/scrapers/"


class SearchApi():

    async def handle(self, request):
        async def get_hotel(sess, url):
            async with sess.get(url) as response:
                return await response.json()

        async def get_hotels():
            queue = []
            async with ClientSession() as sess:
                for hotel in HOTELS:
                    task = asyncio.ensure_future(get_hotel(sess, URL + hotel))
                    queue.append(task)
                responses = await asyncio.gather(*queue)
                ret.append(responses)

        ret = []
        loop = asyncio.get_event_loop()
        await asyncio.ensure_future(get_hotels())

        all_results = ret[0] # 5 x { 'results': [ { hotel1... }, { hotel2... } ... ] }
        merged = []
        for result in all_results:
            merged = self._merge_lists(merged, result['results'])

        return web.json_response({ 'results': merged })

    def _merge_lists(self, merged, next_list):
        if not merged:
            return next_list
        ret = []
        i, j = 0, 0
        while i < len(merged) and j < len(next_list):
            if self._ecstasy(merged[i]) >= self._ecstasy(next_list[j]):
                ret.append(merged[i])
                i += 1
            else:
                ret.append(next_list[j])
                j +=1
        if i < len(merged):
            ret += merged[i:]
        else:
            ret += next_list[j:]
        return ret

    def _ecstasy(self, result_hash):
        return int(result_hash['ecstasy'])


def run():
    app = web.Application()
    handler = SearchApi()
    app.router.add_get('/hotels/search', handler.handle)
    web.run_app(app, port=8000)

if __name__ == "__main__":
    run()
