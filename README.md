iot-GW-solutions
===========

This is a sample client for Intel Gateway Solutions for the IoT development kits

Using the this code and the recipe [Connect an Intel® IoT Gateway to IBM Watson IoT Platform
](https://developer.ibm.com/recipes/tutorials/connect-an-intel-iot-gateway-to-iot-foundation/) listed on https://developer.ibm.com/iot/recipes/, you can quickly showcase how one can connect a Intel IoT Gateway to IBM Watson IoT Platform (WIoTP).

All one needs to do, is to, run a python script which actually sends the cpu utilisation data to the IBM Watson IoT Platform service at http://internetofthings.ibmcloud.com

Refer to the section [Conclusion and other related decipes](https://developer.ibm.com/recipes/tutorials/connect-an-intel-iot-gateway-to-iot-foundation/) in the Watson IoT Recipe [Connect an Intel® IoT Gateway to IBM Watson IoT Platform](https://developer.ibm.com/recipes/tutorials/connect-an-intel-iot-gateway-to-iot-foundation/) that details out on the next set of IoT Recipes that can be followed, to pursue and continue your work, exploring ways to play with IoT Gateway's.

<b><u>Securing the Connections to the Watson IoT Platform</u></b>

The Python script [ibm-iot-quickstart.py](https://github.com/ibm-messaging/iot-gw-solutions/blob/master/samples/ibm-iot-quickstart.py) has been recently modified (last week of Mar, 2017) and has been updated to ensure Secure Connections to Watson IoT Platform (WIoTP). The script prior to this was connecting to WIoTP on 1883. However, going forward, it is recommended to connect to WIoTP using only Secure Connections. The underlying ibmiotf module shall take care of the security aspect, by ensuring that all these Connections are secure.

To have the script successfully executed, you need <b><i>ibmiotf python library</i></b>, to be in place. The following <i>PIP</i> command ensures that this module dependency is met, by setting up the ibmiotf python library. Use sudo privilege to execute the PIP command, as needed.

<b><i>pip install ibmiotf</i></b>
