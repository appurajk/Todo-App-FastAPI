# daily QA reports dashboard App

This Application helps user to show Nightly build reports, it will show everyday report on the header and user can select the date from the calender to view the perticular day reports.

## The report consist of following data on the table :

Test_name: \
No_of_test_cases: \
Passed: \
Failed: \
perofpass: \
Skipped: \
start_time: \
end_time: \
Logfile: \
os_version: \
kernel_version: \
release_version: \
build_version:  \
module_name: \
marker_tag: \

The procedure to setup this Application: \
clone the repository using link
https://gitenterprise.xilinx.com/appurajk/ma35_dashboard.git

Create python environment
    $ python -m venv venv \
    $ source venv/bin/activate \
    $ pip install -r requirements.txt 


MongoDB Driver

$ git clone --branch 1.14.0 https://github.com/mongodb/mongo-c-driver.git \
    && cd mongo-c-driver \
    && mkdir cmake-build \
    && cd cmake-build \
    && cmake -DENABLE_AUTOMATIC_INIT_AND_CLEANUP=OFF .. \
    && make \
    && make install 
    
    
Start the mongodb server<br />
$ mongo

Start ma35_dashboard \
$ cd ma35_dashboard \
$ python main.py

