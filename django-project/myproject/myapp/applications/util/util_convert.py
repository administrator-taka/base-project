def convert_to_milliseconds(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600000 + int(m) * 60000 + int(float(s) * 1000)

