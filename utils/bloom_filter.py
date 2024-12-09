from pybloom_live import ScalableBloomFilter, BloomFilter

def get_bloom_filer(initial_capacity=100, error_rate=0.001):

    BloomFilter()
    return ScalableBloomFilter(initial_capacity=initial_capacity, error_rate=error_rate)

def add_item(bl:ScalableBloomFilter, data):
    bl.add(data)

def is_valid(bl:ScalableBloomFilter, data):
    return data in bl

if __name__ == '__main__':
    f = get_bloom_filer()
    url1 = 'http://www.baidu.com'
    url2 = 'http://qq.com'

    add_item(f, url1)
    print(is_valid(f, url1))
    print(is_valid(f, url2))
    # 可自动扩容的布隆过滤器