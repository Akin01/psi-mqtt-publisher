# Mqtt Client - Publisher

---

This is client publisher to handle sending sensor data to broker.\
I'm using free external broker that provide by **EMQX**.

## Configuration

Here are connection configuration tha i've used :

```
host : broker.emqx.io
port : 8083
```

## Topic

This client contain 6 topic that represent each data will be sending.<br>

| Topic                                   | Purpose                       |
| --------------------------------------- | ----------------------------- |
| `responsi/data/aktuator/temperature`    | sending temperature data      |
| `responsi/data/aktuator/lpgTotal`       | sending total LPG data        |
| `responsi/data/aktuator/numberOfSample` | sending number of sample data |
| `responsi/data/aktuator/Mass`           | sending massa of LPG data     |
| `responsi/data/aktuator/isStop`         | sending status of system      |
| `responsi/data/aktuator/isGas`          | sending status of gas         |

## Installation

To install all library that used on this application, just type `pip install -r requirement.txt` on core project.\
Or if you are using `pipenv` package manager, just type `pipenv install` on core project.
