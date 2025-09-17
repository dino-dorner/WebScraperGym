from flask import Flask, request, render_template
import requests
import datetime

app = Flask(__name__)

class getInfo:

    getCapacity = []
    getNameHours = {}

    def get_JOS(self):
        url = requests.get("https://recsports.osu.edu/fms/Home/GetLocations?locationCode=jos")
        url.raise_for_status()
        sourceData = url.json()
        JOSCap = {}

        for i in range(len(sourceData["locations"])):
            JOSCap[sourceData["locations"][i]["locationName"][3:]] = [int(sourceData["locations"][i]["lastCount"]),int(sourceData["locations"][i]["totalCapacity"]),sourceData["locations"][i]["lastUpdatedDateAndTimeToUniversityFormat"]]
        return JOSCap

    def get_RPAC(self):
        url = requests.get("https://recsports.osu.edu/fms/Home/GetLocations?locationCode=rpac")
        url.raise_for_status()
        sourceData = url.json()
        RPACCap = {}

        for i in range(len(sourceData["locations"])):
            RPACCap[sourceData["locations"][i]["locationName"][4:]] = [int(sourceData["locations"][i]["lastCount"]),int(sourceData["locations"][i]["totalCapacity"]),sourceData["locations"][i]["lastUpdatedDateAndTimeToUniversityFormat"]]
        return RPACCap

    def get_JON(self):
        url = requests.get("https://recsports.osu.edu/fms/Home/GetLocations?locationCode=jon")
        url.raise_for_status()
        sourceData = url.json()
        JONCap = {}

        for i in range(len(sourceData["locations"])):
            JONCap[sourceData["locations"][i]["locationName"][3:]] = [int(sourceData["locations"][i]["lastCount"]),int(sourceData["locations"][i]["totalCapacity"]),sourceData["locations"][i]["lastUpdatedDateAndTimeToUniversityFormat"]]
        return JONCap

    def get_NRC(self):
        url = requests.get("https://recsports.osu.edu/fms/Home/GetLocations?locationCode=nrc")
        url.raise_for_status()
        sourceData = url.json()
        NRCCap = {}

        for i in range(len(sourceData["locations"])):
            NRCCap[sourceData["locations"][i]["locationName"][3:]] = [int(sourceData["locations"][i]["lastCount"]),int(sourceData["locations"][i]["totalCapacity"]),sourceData["locations"][i]["lastUpdatedDateAndTimeToUniversityFormat"]]
        return NRCCap

    def get_ARC(self):
        url = requests.get("https://recsports.osu.edu/fms/Home/GetLocations?locationCode=arc")
        url.raise_for_status()
        sourceData = url.json()
        ARCCap = {}

        for i in range(len(sourceData["locations"])):
            ARCCap[sourceData["locations"][i]["locationName"][3:]] = [int(sourceData["locations"][i]["lastCount"]),int(sourceData["locations"][i]["totalCapacity"]),sourceData["locations"][i]["lastUpdatedDateAndTimeToUniversityFormat"]]
        return ARCCap

    def get_hours(self):
        date = datetime.datetime.now()
        weekday = date.weekday()
        day = date.strftime("%d")
        month = date.strftime("%m")
        year = date.strftime("%Y")

        josurl = requests.get("https://recsports.osu.edu/fms/Home/GetHours?id=4&startDate=" + month + "%2F" + day + "%2F" + year)
        josurl.raise_for_status()
        josJSON = josurl.json()

        rpacurl = requests.get("https://recsports.osu.edu/fms/Home/GetHours?id=3&startDate=" + month + "%2F" + day + "%2F" + year)
        rpacurl.raise_for_status()
        rpacJSON = rpacurl.json()

        nrcurl = requests.get("https://recsports.osu.edu/fms/Home/GetHours?id=5&startDate=" + month + "%2F" + day + "%2F" + year)
        nrcurl.raise_for_status()
        nrcJSON = nrcurl.json()

        arcurl = requests.get("https://recsports.osu.edu/fms/Home/GetHours?id=1&startDate=" + month + "%2F" + day + "%2F" + year)
        arcurl.raise_for_status()
        arcJSON = arcurl.json()

        jonurl = requests.get("https://recsports.osu.edu/fms/Home/GetHours?id=2&startDate=" + month + "%2F" + day + "%2F" + year)
        jonurl.raise_for_status()
        jonJSON = jonurl.json()
        
        josHours = [josJSON["hours"][weekday]["open"],josJSON["hours"][weekday]["close"]]
        rpacHours = [rpacJSON["hours"][weekday]["open"],rpacJSON["hours"][weekday]["close"]]
        nrcHours = [nrcJSON["hours"][weekday]["open"],nrcJSON["hours"][weekday]["close"]]
        arcHours = [arcJSON["hours"][weekday]["open"],arcJSON["hours"][weekday]["close"]]
        jonHours = [jonJSON["hours"][weekday]["open"],jonJSON["hours"][weekday]["close"]]

        self.getNameHours = [["Jesse Owens South", josHours], ["Jesse Owens North", jonHours], ["Adventure Rec. Center", arcHours], ["North Rec. Center", nrcHours], ["RPAC", rpacHours]]



    def getCapMethod(self):
        self.getCapacity = [self.get_JOS(), self.get_JON(), self.get_ARC(), self.get_NRC(), self.get_RPAC()]


@app.route("/")
def home():
    newRequest = getInfo()
    newRequest.getCapMethod()
    newRequest.get_hours()
    return render_template("index.html", osuMetersData=newRequest.getCapacity, osuHoursData=newRequest.getNameHours)


if __name__ == "__main__":
    app.run(debug=True)

