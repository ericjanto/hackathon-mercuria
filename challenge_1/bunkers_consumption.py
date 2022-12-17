# bunkers consumption
consumption = pd.read_csv('consumption.csv', header=None)


def consum(speed, cbm):
    teu = cbm/20
    size = min(10, teu//1000)
    factor = teu/10000
    con = consumption[size-2][np.floor(speed)-18]*max(factor, 1)
    return con
