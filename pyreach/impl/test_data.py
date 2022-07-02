# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Contains test data."""

import json
from typing import Dict, Any


def get_actionsets_json() -> str:
  """Return a test actionsets.json."""
  value_dict = {
      "actions": None,
      "created": "2020-12-02T22:54:17Z",
      "createdBy": "testusertestusertestusertest",
      "version": 6
  }

  actions_dict = [{
      "Name": "FixedCalibration",
      "Preconditions": [],
      "Softstart": False,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "TIPInputs": [],
      "_captureDepthBehavior": "none",
      "_cyclic": True,
      "_intent": "other",
      "_loop": False,
      "_maxAccel": 0.20000000298023224,
      "_maxVelocity": 0.20000000298023224,
      "_steps": [{
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.055156707763671875,
              "y": 0.27040863037109375,
              "z": -0.5407191514968872
          },
          "rot": {
              "w": -0.017183253541588783,
              "x": -0.11628195643424988,
              "y": 0.35665833950042725,
              "z": 0.9268107414245605
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.31074655055999756,
              "y": 0.2453058362007141,
              "z": -0.5561693906784058
          },
          "rot": {
              "w": -0.036141712218523026,
              "x": -0.11852070689201355,
              "y": 0.39984798431396484,
              "z": 0.9081674814224243
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.09024572372436523,
              "y": 0.26927560567855835,
              "z": -0.5438264012336731
          },
          "rot": {
              "w": -0.1222148984670639,
              "x": 0.0014564108569175005,
              "y": 0.46564555168151855,
              "z": 0.8764905333518982
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.1883232593536377,
              "y": 0.24803876876831055,
              "z": -0.556236982345581
          },
          "rot": {
              "w": -0.27006784081459045,
              "x": -0.02783861570060253,
              "y": 0.4526783227920532,
              "z": 0.8493354916572571
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.137556791305542,
              "y": 0.2228027582168579,
              "z": -0.6603227257728577
          },
          "rot": {
              "w": -0.39041873812675476,
              "x": -0.2338070124387741,
              "y": 0.24998824298381805,
              "z": 0.8546422719955444
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.02150106430053711,
              "y": 0.33569109439849854,
              "z": -0.639304518699646
          },
          "rot": {
              "w": -0.02734074927866459,
              "x": 0.020983664318919182,
              "y": 0.27115345001220703,
              "z": 0.9619189500808716
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.20204555988311768,
              "y": 0.3192251920700073,
              "z": -0.7481116652488708
          },
          "rot": {
              "w": 0.32907429337501526,
              "x": 0.15011605620384216,
              "y": 0.14176903665065765,
              "z": 0.9214536547660828
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.17734229564666748,
              "y": 0.31349778175354004,
              "z": -0.6484332084655762
          },
          "rot": {
              "w": 0.37002721428871155,
              "x": 0.32440489530563354,
              "y": 0.16082245111465454,
              "z": 0.855556845664978
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.06824016571044922,
              "y": 0.34116923809051514,
              "z": -0.5412105321884155
          },
          "rot": {
              "w": 0.32899510860443115,
              "x": 0.263325035572052,
              "y": 0.3091835081577301,
              "z": 0.8525419235229492
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.07199680805206299,
              "y": 0.3234095573425293,
              "z": -0.500237762928009
          },
          "rot": {
              "w": 0.018354417756199837,
              "x": 0.04819842055439949,
              "y": 0.48600322008132935,
              "z": 0.8724339604377747
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.08173477649688721,
              "y": 0.3319023847579956,
              "z": -0.5488678216934204
          },
          "rot": {
              "w": 0.013053130358457565,
              "x": 0.3119683563709259,
              "y": 0.4293849468231201,
              "z": 0.8474279046058655
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.08409905433654785,
              "y": 0.27482062578201294,
              "z": -0.4851151406764984
          },
          "rot": {
              "w": -0.24585236608982086,
              "x": -0.16035090386867523,
              "y": 0.3901900351047516,
              "z": 0.8726946711540222
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.16621875762939453,
              "y": 0.2913582921028137,
              "z": -0.595568835735321
          },
          "rot": {
              "w": -0.22161543369293213,
              "x": 0.17923307418823242,
              "y": 0.42937320470809937,
              "z": 0.8569718599319458
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.055191993713378906,
              "y": 0.3450812101364136,
              "z": -0.6489378809928894
          },
          "rot": {
              "w": -0.11483451724052429,
              "x": 0.06677353382110596,
              "y": 0.3458213806152344,
              "z": 0.9288498163223267
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.12487900257110596,
              "y": 0.3032267093658447,
              "z": -0.6225184202194214
          },
          "rot": {
              "w": -0.1085314154624939,
              "x": -0.22458617389202118,
              "y": 0.38407206535339355,
              "z": 0.8889716863632202
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.23992621898651123,
              "y": 0.30920612812042236,
              "z": -0.4970511496067047
          },
          "rot": {
              "w": -0.16518068313598633,
              "x": -0.46570122241973877,
              "y": 0.3053218126296997,
              "z": 0.8140125274658203
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.016614437103271484,
              "y": 0.2758892774581909,
              "z": -0.5372304916381836
          },
          "rot": {
              "w": -0.08328774571418762,
              "x": -0.09272008389234543,
              "y": 0.49821940064430237,
              "z": 0.8580464124679565
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.12767696380615234,
              "y": 0.32739776372909546,
              "z": -0.7407230138778687
          },
          "rot": {
              "w": -0.25639763474464417,
              "x": -0.1105615645647049,
              "y": 0.15697912871837616,
              "z": 0.9473087787628174
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.00080108642578125,
              "y": 0.3821737766265869,
              "z": -0.5630264282226562
          },
          "rot": {
              "w": 0.0045214151032269,
              "x": 0.02442082017660141,
              "y": 0.21607095003128052,
              "z": 0.9760617613792419
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.18361878395080566,
              "y": 0.32750993967056274,
              "z": -0.699981153011322
          },
          "rot": {
              "w": 0.013933375477790833,
              "x": -0.026064973324537277,
              "y": 0.22241060435771942,
              "z": 0.9745050072669983
          }
      }],
      "_successType": "other"
  }, {
      "Name": "SingulateLeftBin",
      "Preconditions": [],
      "Softstart": False,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "TIPInputs": [{
          "Dimensions": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "LocalGOPos": {
              "x": -0.1980351209640503,
              "y": -0.1331457793712616,
              "z": -0.6422970294952393
          },
          "LocalGORot": {
              "w": 0.7126560807228088,
              "x": -0.7008927464485168,
              "y": -0.025330642238259315,
              "z": -0.015135188587009907
          },
          "Name": "Torus0",
          "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
          "PickData": {
              "depthTS": 0,
              "deviceName": "",
              "deviceType": "",
              "label": "",
              "pose2D": {
                  "x": 0.0,
                  "y": 0.0
              },
              "position3D": {
                  "x": 0.0,
                  "y": 0.0,
                  "z": 0.0
              },
              "quaternion3D": {
                  "w": 0.0,
                  "x": 0.0,
                  "y": 0.0,
                  "z": 0.0
              },
              "tags": [],
              "userTS": 0
          },
          "TIPObjectType": "Torus",
          "TIPPos": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "TIPRot": {
              "w": 1.0,
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          }
      }],
      "_captureDepthBehavior": "none",
      "_cyclic": False,
      "_intent": "pick",
      "_loop": False,
      "_maxAccel": 8.0,
      "_maxVelocity": 2.0,
      "_steps": [{
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": -1,
          "_parentType": 1,
          "_radius": 0.05000000074505806,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setDigitalIO": True,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": True,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": 0,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.15014392137527466,
              "y": 0.1842595636844635,
              "z": 10.78434944152832
          },
          "rot": {
              "w": -1.0,
              "x": 2.9802322387695312e-08,
              "y": -2.7939677238464355e-08,
              "z": 5.774199962615967e-08
          }
      }, {
          "_acceleration": 4.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": True,
          "_parentStepIdx": -1,
          "_parentType": 1,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": 0,
          "_useForceMode": False,
          "_useProcessMode": True,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 1.0,
          "_wait": 0.10000000149011612,
          "pos": {
              "x": -3.9113099774112925e-05,
              "y": 0.00011130343773402274,
              "z": 6.100447080825688e-06
          },
          "rot": {
              "w": -1.0,
              "x": 2.9802322387695312e-08,
              "y": -2.7939677238464355e-08,
              "z": 5.774199962615967e-08
          }
      }, {
          "_acceleration": 4.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": True,
          "_parentStepIdx": -1,
          "_parentType": 1,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": 0,
          "_useForceMode": False,
          "_useProcessMode": True,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 1.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.22111254930496216,
              "y": -2.03483247756958,
              "z": 14.018765449523926
          },
          "rot": {
              "w": -0.9973260760307312,
              "x": -0.06723517179489136,
              "y": 0.004309169948101044,
              "z": 0.02831348031759262
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": -1,
          "_parentType": 0,
          "_radius": 0.05000000074505806,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.0131511390209198,
              "y": 0.1529742032289505,
              "z": -0.6136351823806763
          },
          "rot": {
              "w": -0.012394964694976807,
              "x": -0.01839575171470642,
              "y": -0.00471101887524128,
              "z": 0.9997429251670837
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": -1,
          "_parentType": 0,
          "_radius": 0.029999999329447746,
          "_randomizedOffset": True,
          "_randomizedOffsetRadiusCM": 6.0,
          "_setCapability": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": False,
          "_setDigitalIO": True,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.36913561820983887,
              "y": 0.08218996971845627,
              "z": -0.6369068622589111
          },
          "rot": {
              "w": 0.018659118562936783,
              "x": -0.01261720061302185,
              "y": -0.031854793429374695,
              "z": 0.9992386698722839
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": -1,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_setCapabilityName": "",
          "_setCapabilityType": "blowoff",
          "_setCapabilityValue": False,
          "_setDigitalIO": True,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.03844594955444336,
              "y": 0.16870592534542084,
              "z": -0.5015764832496643
          },
          "rot": {
              "w": 0.018659118562936783,
              "x": -0.01261720061302185,
              "y": -0.031854793429374695,
              "z": 0.9992386698722839
          }
      }],
      "_successType": "vacuum-pressure-sensor"
  }, {
      "Name": "SingulateRightBin",
      "Preconditions": [],
      "Softstart": False,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "TIPInputs": [{
          "Dimensions": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "LocalGOPos": {
              "x": 0.215956449508667,
              "y": -0.13462474942207336,
              "z": -0.7082916498184204
          },
          "LocalGORot": {
              "w": 0.6977351307868958,
              "x": -0.7160830497741699,
              "y": -0.004250542260706425,
              "z": 0.019307635724544525
          },
          "Name": "Torus0",
          "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
          "PickData": {
              "depthTS": 0,
              "deviceName": "",
              "deviceType": "",
              "label": "",
              "pose2D": {
                  "x": 0.0,
                  "y": 0.0
              },
              "position3D": {
                  "x": 0.0,
                  "y": 0.0,
                  "z": 0.0
              },
              "quaternion3D": {
                  "w": 0.0,
                  "x": 0.0,
                  "y": 0.0,
                  "z": 0.0
              },
              "tags": [],
              "userTS": 0
          },
          "TIPObjectType": "Torus",
          "TIPPos": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "TIPRot": {
              "w": 1.0,
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          }
      }],
      "_captureDepthBehavior": "none",
      "_cyclic": False,
      "_intent": "pick",
      "_loop": False,
      "_maxAccel": 8.0,
      "_maxVelocity": 2.0,
      "_steps": [{
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": -1,
          "_parentType": 1,
          "_radius": 0.05000000074505806,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setDigitalIO": True,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": True,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": 0,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.5086552500724792,
              "y": -0.40456056594848633,
              "z": 15.381595611572266
          },
          "rot": {
              "w": -1.0,
              "x": 2.6822084464583895e-07,
              "y": -1.862644793959589e-08,
              "z": 3.1315713044932636e-07
          }
      }, {
          "_acceleration": 4.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": True,
          "_parentStepIdx": -1,
          "_parentType": 1,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": 0,
          "_useForceMode": False,
          "_useProcessMode": True,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 1.0,
          "_wait": 0.10000000149011612,
          "pos": {
              "x": 8.212205284507945e-05,
              "y": 0.00018972481484524906,
              "z": -2.605909321573563e-05
          },
          "rot": {
              "w": -1.0,
              "x": 2.6822084464583895e-07,
              "y": -1.862644793959589e-08,
              "z": 3.1315713044932636e-07
          }
      }, {
          "_acceleration": 4.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": True,
          "_parentStepIdx": -1,
          "_parentType": 1,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": 0,
          "_useForceMode": False,
          "_useProcessMode": True,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 1.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.5743547677993774,
              "y": -0.4567742347717285,
              "z": 17.367746353149414
          },
          "rot": {
              "w": -1.0,
              "x": 2.6822084464583895e-07,
              "y": -1.862644793959589e-08,
              "z": 3.1315713044932636e-07
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.05000000074505806,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": 0.013564735651016235,
              "y": 0.18092398345470428,
              "z": -0.654334545135498
          },
          "rot": {
              "w": 0.019034862518310547,
              "x": 0.027513116598129272,
              "y": 0.0007397201843559742,
              "z": 0.9994399547576904
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.029999999329447746,
          "_randomizedOffset": True,
          "_randomizedOffsetRadiusCM": 6.0,
          "_setCapability": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": False,
          "_setDigitalIO": True,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.31923291087150574,
              "y": 0.096033975481987,
              "z": -0.6445804238319397
          },
          "rot": {
              "w": 0.025822922587394714,
              "x": -0.04089435935020447,
              "y": -0.005485633388161659,
              "z": 0.9988147020339966
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_setCapabilityName": "",
          "_setCapabilityType": "blowoff",
          "_setCapabilityValue": False,
          "_setDigitalIO": True,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.002480417490005493,
              "y": 0.1664791703224182,
              "z": -0.5675230622291565
          },
          "rot": {
              "w": 0.025822922587394714,
              "x": -0.04089435935020447,
              "y": -0.005485633388161659,
              "z": 0.9988147020339966
          }
      }],
      "_successType": "vacuum-pressure-sensor"
  }, {
      "Name": "StowSuction1",
      "Preconditions": [],
      "Softstart": True,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "TIPInputs": [],
      "_captureDepthBehavior": "none",
      "_cyclic": False,
      "_intent": "other",
      "_loop": False,
      "_maxAccel": 0.20000000298023224,
      "_maxVelocity": 0.20000000298023224,
      "_steps": [{
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.10489892959594727,
              "y": 0.23676621913909912,
              "z": -0.3586924076080322
          },
          "rot": {
              "w": 0.0013059101765975356,
              "x": 5.96978425164707e-05,
              "y": 5.684150164597668e-05,
              "z": 0.9999991655349731
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.10490000247955322,
              "y": 0.28263533115386963,
              "z": -0.28039950132369995
          },
          "rot": {
              "w": -4.371138828673793e-08,
              "x": 1.0865025545925278e-09,
              "y": -4.749253516506268e-17,
              "z": 1.0
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.10490000247955322,
              "y": 0.17086505889892578,
              "z": -0.28039950132369995
          },
          "rot": {
              "w": -4.371138828673793e-08,
              "x": 1.0865025545925278e-09,
              "y": -4.749253516506268e-17,
              "z": 1.0
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.10490000247955322,
              "y": 0.17086505889892578,
              "z": -0.3569999933242798
          },
          "rot": {
              "w": -4.371138828673793e-08,
              "x": 1.0865025545925278e-09,
              "y": -4.749253516506268e-17,
              "z": 1.0
          }
      }, {
          "_acceleration": 0.0,
          "_delay": 0.0,
          "_individualVelocityAcceleration": False,
          "_parentStepIdx": 0,
          "_parentType": 0,
          "_radius": 0.0,
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_setCapability": False,
          "_setCapabilityIOType": "",
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIO": False,
          "_setToolDigitalIONumber": 0,
          "_setToolDigitalIOValue": False,
          "_tipInputIdx": -1,
          "_useForceMode": False,
          "_useProcessMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_velocity": 0.0,
          "_wait": 0.0,
          "pos": {
              "x": -0.10490000247955322,
              "y": 0.24087250232696533,
              "z": -0.3569999933242798
          },
          "rot": {
              "w": -4.371138828673793e-08,
              "x": 1.0865025545925278e-09,
              "y": -4.749253516506268e-17,
              "z": 1.0
          }
      }],
      "_successType": "other"
  }]

  actions_string = json.dumps(actions_dict, indent=None, separators=(",", ":"))
  value_dict["actions"] = actions_string
  return json.dumps(value_dict, indent=None, separators=(",", ":"))


def get_calibration_json() -> str:
  """Return a test calibration.json."""
  devices_dict: Dict[str, Any] = {
      "devices": [{
          "deviceName": "",
          "deviceType": "color-camera",
          "parameters": {
              "distortion": [
                  -0.3970008552803565, 0.22101876820872876,
                  -0.00043916833522675286, 0.0007154189097855913,
                  -0.10688964800826162
              ],
              "extrinsics": [
                  -0.28965950169824467, -0.729105109844089, 0.5411210177892349,
                  3.035434604577181, 0.11426984572344681, 0.6672967717093193
              ],
              "extrinsicsResidual": 0,
              "height": 480,
              "intrinsics": [
                  481.3731063491299, 641.0884215185575, 323.47375401648327,
                  237.04241976917518
              ],
              "intrinsicsResidual": 0.44558846473129016,
              "lensModel": "pinhole",
              "width": 640
          }
      }, {
          "deviceName": "",
          "deviceType": "depth-camera",
          "parameters": {
              "distortion": [
                  0.10482133276534181, -0.08769739332199046,
                  -0.0013728557869843911, -0.00027400197754087464,
                  0.038613921807643656
              ],
              "distortionDepth": [
                  0.006488360238356572, 9.882108464184608e-05, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0
              ],
              "extrinsics": [
                  0.03334450773087864, -0.7665406156951181, 0.5560341645617256,
                  -3.1019944979760594, 0.03153497484672315, -0.0302886657855227
              ],
              "extrinsicsResidual": 2.547426978391909,
              "height": 720,
              "intrinsics": [
                  622.92432388711, 622.6435812426041, 639.1354839894639,
                  365.21509119261384
              ],
              "intrinsicsResidual": 0.5427200751494077,
              "lensModel": "pinhole",
              "width": 1280
          }
      }, {
          "deviceName": "bodyTag",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  0.000430357232698349, -0.056926297692693646,
                  0.09958558371014069, 1.2154564623508188, 1.1869818397246061,
                  -1.2125578770150043
              ],
              "extrinsicsResidual": 2.547426978391909,
              "id": 100,
              "intrinsics": [0.04095, 0.04095, 0],
              "linkName": "wrist_2_link",
              "toolMount": "ur"
          }
      }, {
          "deviceName": "bodyTag.robot",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  0.000430357232698349, -0.056926297692693646,
                  0.09958558371014069, 1.2154564623508188, 1.1869818397246061,
                  -1.2125578770150043
              ],
              "extrinsicsResidual": 2.547426978391909,
              "id": 100,
              "intrinsics": [0.04095, 0.04095, 0],
              "linkName": "wrist_2_link",
              "toolMount": "robot"
          }
      }, {
          "deviceName": "tip.ur",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  0.004453485238087255, -0.055702600244064024,
                  0.1626512213476071, 0, 0, 0
              ],
              "extrinsicsAdjust": [0, 0, -0.005, 0, 0, 0],
              "intrinsics": [0.04, 0.04, 0.001],
              "subType": "tip",
              "toolMount": "ur"
          }
      }, {
          "deviceName": "",
          "deviceType": "photoneo",
          "parameters": {
              "distortion": [
                  0.10482133276534181, -0.08769739332199046,
                  -0.0013728557869843911, -0.00027400197754087464,
                  0.038613921807643656
              ],
              "distortionDepth": [
                  0.006488360238356572, 9.882108464184608e-05, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0
              ],
              "extrinsics": [
                  0.03334450773087864, -0.7665406156951181, 0.5560341645617256,
                  -3.1019944979760594, 0.03153497484672315, -0.0302886657855227
              ],
              "extrinsicsResidual": 2.547426978391909,
              "height": 720,
              "intrinsics": [
                  622.92432388711, 622.6435812426041, 639.1354839894639,
                  365.21509119261384
              ],
              "intrinsicsResidual": 0.5427200751494077,
              "lensModel": "pinhole",
              "width": 1280
          }
      }, {
          "deviceName": "",
          "deviceType": "robot",
          "parameters": {
              "calibrationAction": [
                  [
                      1.56049239635468, -1.47792708873749, 1.64017152786255,
                      -1.97951197624207, 4.39641571044922, 0.0125926649197936
                  ],
                  [
                      1.372989177703857, -1.104734258060791, 1.445080105458395,
                      -0.8562386792949219, 4.590588092803955,
                      -0.3420522848712366
                  ],
                  [
                      1.650985240936279, -0.6145833295634766, 1.110745255147116,
                      -1.878090520898336, 5.671570777893066, -0.117683235798971
                  ],
                  [
                      1.469185352325439, -0.6274870199016114, 1.120287720357076,
                      -1.871598859826559, 5.577063083648682, -0.1108835379229944
                  ],
                  [
                      1.261108875274658, -0.6807425779155274, 1.114529434834616,
                      -2.008906980554098, 5.348403453826904, -0.11096698442568
                  ],
                  [
                      1.349345684051514, -0.7796028417399903, 1.113798920308248,
                      -2.050168653527731, 4.886090278625488, -0.1110032240497034
                  ],
                  [
                      1.349369525909424, -0.5888841909221192, 1.113547150288717,
                      -2.392721792260641, 4.886281967163086, -0.11096698442568
                  ],
                  [
                      1.349345684051514, -0.5427449506572266, 1.113547150288717,
                      -2.468518396417135, 5.162521362304688, -0.1109073797809046
                  ],
                  [
                      1.245808601379395, -0.5889919561198731, 1.113714996968405,
                      -2.337427755395407, 5.161922454833984, -0.1110151449786585
                  ],
                  [
                      1.245832443237305, -0.5889681142619629, 1.113726441060201,
                      -2.337403913537496, 5.161922454833984, -0.1110385099994105
                  ],
                  [
                      1.246216297149658, -0.5888365072062989, 1.100868050252096,
                      -2.354394098321432, 4.596005439758301, -0.111086670552389
                  ],
                  [
                      1.324470043182373, -0.6204608243754883, 1.10163385072817,
                      -2.299032827416891, 3.91244649887085, -0.1111462751971644
                  ],
                  [
                      1.484946727752686, -0.6157444280437012, 1.104280296956198,
                      -2.209009786645407, 3.912075042724609, -0.1109431425677698
                  ],
                  [
                      1.623321533203125, -0.6158760350993653, 1.103909317647116,
                      -2.209129949609274, 3.912314653396606, -0.1109550634967249
                  ],
                  [
                      1.664713382720947, -0.6160200399211426, 1.103765312825338,
                      -2.209321161309713, 4.194935321807861, -0.1109073797809046
                  ],
                  [
                      1.688446044921875, -0.5890878003886719, 1.103705231343405,
                      -2.471793790856832, 4.422881126403809, -0.1108954588519495
                  ],
                  [
                      1.633677005767822, -0.7347205442241211, 1.284302059804098,
                      -2.558526655236715, 4.422844886779785, -0.1108358542071741
                  ],
                  [
                      1.488794326782227, -0.8030474942973633, 1.40239936510195,
                      -2.558431287805075, 4.878581523895264, -0.1109431425677698
                  ],
                  [
                      1.288054943084717, -0.8350256246379395, 1.51362640062441,
                      -2.387800355950827, 5.362728118896484, -0.2145565191852015
                  ],
                  [
                      1.246132373809814, -0.9281223577312012, 1.51003867784609,
                      -1.729917188683981, 5.342055320739746, -0.2146042029010218
                  ],
                  [
                      1.202383518218994, -0.957451657657959, 1.509115521107809,
                      -1.5496462148479, 5.22432804107666, -0.214639965687887
                  ],
                  [
                      1.272443294525146, -0.9715579313090821, 1.407652203236715,
                      -1.22933657587085, 4.720445156097412, -0.5781443754779261
                  ],
                  [
                      1.285038471221924, -0.9626768392375489, 1.406803433095114,
                      -1.325238065128662, 4.312658786773682, -0.6388657728778284
                  ],
                  [
                      1.356053352355957, -0.8769400876811524, 1.273212734852926,
                      -1.325526074772217, 4.091338634490967, -0.7849581877337855
                  ],
                  [
                      1.464151382446289, -0.7035597127727051, 1.090534989033834,
                      -1.501897649174072, 3.891079902648926, -0.9476130644427698
                  ],
                  [
                      1.571114063262939, -0.7405117315104981, 1.090786759053366,
                      -1.794917722741598, 4.132608890533447, -0.94763690630068
                  ]
              ],
              "calibrationPose": {
                  "cartesian": [
                      0.10407050653071281, 0.7023423308223661,
                      0.15673661720667226, -3.0832317489960137,
                      0.3292858551488942, 0.17547197814873564
                  ],
                  "joints": [
                      1.598235130310059, -2.286548276940817, -1.490765571594238,
                      -0.8842314046672364, 1.677998065948486, 0.2429585456848145
                  ]
              },
              "extrinsics": [0.1, 0, 0, 0, 0, 0],
              "extrinsicsResidual": 2.547426978391909,
              "urdf": "ur5e.urdf"
          }
      }, {
          "deviceName": "",
          "deviceType": "ur",
          "parameters": {
              "calibrationAction": [
                  [
                      1.56049239635468, -1.47792708873749, 1.64017152786255,
                      -1.97951197624207, 4.39641571044922, 0.0125926649197936
                  ],
                  [
                      1.372989177703857, -1.104734258060791, 1.445080105458395,
                      -0.8562386792949219, 4.590588092803955,
                      -0.3420522848712366
                  ],
                  [
                      1.650985240936279, -0.6145833295634766, 1.110745255147116,
                      -1.878090520898336, 5.671570777893066, -0.117683235798971
                  ],
                  [
                      1.469185352325439, -0.6274870199016114, 1.120287720357076,
                      -1.871598859826559, 5.577063083648682, -0.1108835379229944
                  ],
                  [
                      1.261108875274658, -0.6807425779155274, 1.114529434834616,
                      -2.008906980554098, 5.348403453826904, -0.11096698442568
                  ],
                  [
                      1.349345684051514, -0.7796028417399903, 1.113798920308248,
                      -2.050168653527731, 4.886090278625488, -0.1110032240497034
                  ],
                  [
                      1.349369525909424, -0.5888841909221192, 1.113547150288717,
                      -2.392721792260641, 4.886281967163086, -0.11096698442568
                  ],
                  [
                      1.349345684051514, -0.5427449506572266, 1.113547150288717,
                      -2.468518396417135, 5.162521362304688, -0.1109073797809046
                  ],
                  [
                      1.245808601379395, -0.5889919561198731, 1.113714996968405,
                      -2.337427755395407, 5.161922454833984, -0.1110151449786585
                  ],
                  [
                      1.245832443237305, -0.5889681142619629, 1.113726441060201,
                      -2.337403913537496, 5.161922454833984, -0.1110385099994105
                  ],
                  [
                      1.246216297149658, -0.5888365072062989, 1.100868050252096,
                      -2.354394098321432, 4.596005439758301, -0.111086670552389
                  ],
                  [
                      1.324470043182373, -0.6204608243754883, 1.10163385072817,
                      -2.299032827416891, 3.91244649887085, -0.1111462751971644
                  ],
                  [
                      1.484946727752686, -0.6157444280437012, 1.104280296956198,
                      -2.209009786645407, 3.912075042724609, -0.1109431425677698
                  ],
                  [
                      1.623321533203125, -0.6158760350993653, 1.103909317647116,
                      -2.209129949609274, 3.912314653396606, -0.1109550634967249
                  ],
                  [
                      1.664713382720947, -0.6160200399211426, 1.103765312825338,
                      -2.209321161309713, 4.194935321807861, -0.1109073797809046
                  ],
                  [
                      1.688446044921875, -0.5890878003886719, 1.103705231343405,
                      -2.471793790856832, 4.422881126403809, -0.1108954588519495
                  ],
                  [
                      1.633677005767822, -0.7347205442241211, 1.284302059804098,
                      -2.558526655236715, 4.422844886779785, -0.1108358542071741
                  ],
                  [
                      1.488794326782227, -0.8030474942973633, 1.40239936510195,
                      -2.558431287805075, 4.878581523895264, -0.1109431425677698
                  ],
                  [
                      1.288054943084717, -0.8350256246379395, 1.51362640062441,
                      -2.387800355950827, 5.362728118896484, -0.2145565191852015
                  ],
                  [
                      1.246132373809814, -0.9281223577312012, 1.51003867784609,
                      -1.729917188683981, 5.342055320739746, -0.2146042029010218
                  ],
                  [
                      1.202383518218994, -0.957451657657959, 1.509115521107809,
                      -1.5496462148479, 5.22432804107666, -0.214639965687887
                  ],
                  [
                      1.272443294525146, -0.9715579313090821, 1.407652203236715,
                      -1.22933657587085, 4.720445156097412, -0.5781443754779261
                  ],
                  [
                      1.285038471221924, -0.9626768392375489, 1.406803433095114,
                      -1.325238065128662, 4.312658786773682, -0.6388657728778284
                  ],
                  [
                      1.356053352355957, -0.8769400876811524, 1.273212734852926,
                      -1.325526074772217, 4.091338634490967, -0.7849581877337855
                  ],
                  [
                      1.464151382446289, -0.7035597127727051, 1.090534989033834,
                      -1.501897649174072, 3.891079902648926, -0.9476130644427698
                  ],
                  [
                      1.571114063262939, -0.7405117315104981, 1.090786759053366,
                      -1.794917722741598, 4.132608890533447, -0.94763690630068
                  ]
              ],
              "calibrationPose": {
                  "cartesian": [
                      0.10407050653071281, 0.7023423308223661,
                      0.15673661720667226, -3.0832317489960137,
                      0.3292858551488942, 0.17547197814873564
                  ],
                  "joints": [
                      1.598235130310059, -2.286548276940817, -1.490765571594238,
                      -0.8842314046672364, 1.677998065948486, 0.2429585456848145
                  ]
              },
              "extrinsics": [0, 0, 0, 0, 0, 0],
              "extrinsicsResidual": 2.547426978391909,
              "urdf": "ur5e.urdf"
          }
      }, {
          "deviceName": "",
          "deviceType": "uvc",
          "parameters": {
              "distortion": [
                  -0.3970008552803565, 0.22101876820872876,
                  -0.00043916833522675286, 0.0007154189097855913,
                  -0.10688964800826162
              ],
              "extrinsics": [
                  -0.28965950169824467, -0.729105109844089, 0.5411210177892349,
                  3.035434604577181, 0.11426984572344681, 0.6672967717093193
              ],
              "extrinsicsResidual": 0,
              "height": 480,
              "intrinsics": [
                  481.3731063491299, 641.0884215185575, 323.47375401648327,
                  237.04241976917518
              ],
              "intrinsicsResidual": 0.44558846473129016,
              "lensModel": "pinhole",
              "width": 640
          }
      }],
      "robot-name": "python-local-test",
      "timestamp": 1606954076.3175173,
      "version": 20190118
  }

  return json.dumps(devices_dict)


def get_robot_constraints_json() -> str:
  """Return a test robot_constraints.json."""
  robot_constraints = {
      "devices": [{
          "deviceType": "robot",
          "parameters": {
              "jointLimits": [[-363.0000016970871, 363.00000013981145],
                              [-363.0000016970871, 363.00000013981145],
                              [-363.0000016970871, 363.00000013981145],
                              [-363.0000016970871, 363.00000013981145],
                              [-363.0000016970871, 363.00000013981145],
                              [-363.0000016970871, 363.00000013981145]],
          }
      }],
      "version": 20200101,
  }
  return json.dumps(robot_constraints)


def get_workcell_constraints_json() -> str:
  """Return a test workcell_constraints.json."""
  devices_dict: Dict[str, Any] = {
      "devices": [{
          "deviceType": "robot",
          "parameters": {
              "referencePoses": {
                  "ikhint1": {
                      "type":
                          "none",
                      "pose": [
                          1.33904457092285, -1.30520141124725, 1.83943212032318,
                          -2.18432211875916, 4.76191997528076,
                          -0.295647442340851
                      ]
                  },
                  "ikhint2": {
                      "type":
                          "none",
                      "pose": [
                          1.3390326499939, -1.30521333217621, 1.83942067623138,
                          -2.18433356285095, 4.76193189620972,
                          -0.295647442340851
                      ]
                  },
                  "ikhint3": {
                      "type":
                          "none",
                      "pose": [
                          1.33897256851196, -1.30512940883636, 1.83931195735931,
                          -2.18429780006409, 4.76188373565674,
                          -0.295707523822784
                      ]
                  },
                  "ikhint4": {
                      "type":
                          "none",
                      "pose": [
                          1.33897256851196, -1.30514132976532, 1.83931195735931,
                          -2.18429780006409, 4.76191997528076,
                          -0.295671761035919
                      ]
                  },
                  "ikhint5": {
                      "type":
                          "none",
                      "pose": [
                          1.33898496627808, -1.30515325069427, 1.83931195735931,
                          -2.18427348136902, 4.76190805435181, -0.29571944475174
                      ]
                  },
                  "ikhint6": {
                      "type":
                          "none",
                      "pose": [
                          1.33898496627808, -1.30517756938934, 1.83931195735931,
                          -2.18427348136902, 4.76193189620972,
                          -0.295695602893829
                      ]
                  },
                  "ikhint7": {
                      "type":
                          "none",
                      "pose": [
                          1.33899688720703, -1.30515325069427, 1.83928716182709,
                          -2.18432211875916, 4.76191997528076, -0.29571944475174
                      ]
                  },
                  "ikhint8": {
                      "type":
                          "none",
                      "pose": [
                          1.33897256851196, -1.30516517162323, 1.83930051326752,
                          -2.18432211875916, 4.76188373565674,
                          -0.295707523822784
                      ]
                  },
                  "ikhint9": {
                      "type":
                          "none",
                      "pose": [
                          1.3390326499939, -1.30515325069427, 1.83930051326752,
                          -2.18427348136902, 4.76191997528076,
                          -0.295671761035919
                      ]
                  },
                  "ikhint10": {
                      "type":
                          "none",
                      "pose": [
                          1.33900880813599, -1.30515325069427, 1.83928716182709,
                          -2.18429780006409, 4.76190805435181,
                          -0.295695602893829
                      ]
                  },
                  "ikhint11": {
                      "type":
                          "none",
                      "pose": [
                          1.33900880813599, -1.30512940883636, 1.83930051326752,
                          -2.18429780006409, 4.76190805435181,
                          -0.295695602893829
                      ]
                  },
                  "ikhint12": {
                      "type":
                          "none",
                      "pose": [
                          1.33899688720703, -1.30516517162323, 1.83931195735931,
                          -2.18426203727722, 4.76193189620972,
                          -0.295695602893829
                      ]
                  },
                  "ikhint13": {
                      "type":
                          "none",
                      "pose": [
                          1.33899688720703, -1.30514132976532, 1.83931195735931,
                          -2.18433356285095, 4.76191997528076,
                          -0.295707523822784
                      ]
                  },
                  "ikhint14": {
                      "type":
                          "none",
                      "pose": [
                          1.33898496627808, -1.30515325069427, 1.83932340145111,
                          -2.18429780006409, 4.76193189620972,
                          -0.295731365680695
                      ]
                  },
              },
          },
      }, {
          "deviceName": "LeftBin",
          "deviceType": "object",
          "parameters": {
              "geometry": {
                  "type":
                      "composite",
                  "subtype":
                      "bin",
                  "position": {
                      "x": -0.24138717353344,
                      "y": -0.705161988735199,
                      "z": -0.178804665803909
                  },
                  "rotation": {
                      "rx": 359.544708251953,
                      "ry": 358.477264404297,
                      "rz": 89.6418685913086
                  },
                  "geometries": [{
                      "type": "box",
                      "scale": {
                          "x": 0.28000009059906,
                          "y": 0.379999577999115,
                          "z": 0.00450000213459134
                      },
                      "position": {
                          "x": -1.99943315237761e-07,
                          "y": 1.8533319234848e-07,
                          "z": -0.0749999582767487
                      },
                      "rotation": {
                          "rx": 2.9882073704357e-06,
                          "ry": -2.13443385632672e-07,
                          "rz": -5.56596911640531e-15
                      }
                  }, {
                      "type": "box",
                      "scale": {
                          "x": 0.280000150203705,
                          "y": 0.02659996971488,
                          "z": 0.150000259280205
                      },
                      "position": {
                          "x": -4.41214069724083e-08,
                          "y": -0.189999714493752,
                          "z": -1.3029421097599e-08
                      },
                      "rotation": {
                          "rx": 0,
                          "ry": 0,
                          "rz": 0
                      }
                  }, {
                      "type": "box",
                      "scale": {
                          "x": 0.280000150203705,
                          "y": 0.02659996971488,
                          "z": 0.150000259280205
                      },
                      "position": {
                          "x": -7.5087882578373e-08,
                          "y": 0.189999848604202,
                          "z": 1.58070179168135e-08
                      },
                      "rotation": {
                          "rx": 0,
                          "ry": 0,
                          "rz": 0
                      }
                  }, {
                      "type": "box",
                      "scale": {
                          "x": 0.0196000020951033,
                          "y": 0.37999951839447,
                          "z": 0.150000259280205
                      },
                      "position": {
                          "x": 0.139999702572823,
                          "y": 1.49011611938477e-08,
                          "z": 3.72529029846191e-09
                      },
                      "rotation": {
                          "rx": 0,
                          "ry": 0,
                          "rz": 0
                      }
                  }, {
                      "type": "box",
                      "scale": {
                          "x": 0.0196000020951033,
                          "y": 0.37999951839447,
                          "z": 0.150000259280205
                      },
                      "position": {
                          "x": -0.140000060200691,
                          "y": 7.45058059692383e-08,
                          "z": -4.19095158576965e-09
                      },
                      "rotation": {
                          "rx": 0,
                          "ry": 0,
                          "rz": 0
                      }
                  }]
              }
          }
      }, {
          "deviceName": "RightBin",
          "deviceType": "object",
          "parameters": {
              "geometry": {
                  "type":
                      "composite",
                  "subtype":
                      "bin",
                  "position": {
                      "x": 0.25575715303421,
                      "y": -0.709752559661865,
                      "z": -0.176420882344246
                  },
                  "rotation": {
                      "rx": 0.814474105834961,
                      "ry": 359.750946044922,
                      "rz": 90.0870208740234
                  },
                  "geometries": [{
                      "type": "box",
                      "scale": {
                          "x": 0.279999971389771,
                          "y": 0.38000026345253,
                          "z": 0.00449999840930104
                      },
                      "position": {
                          "x": -1.38621544465423e-07,
                          "y": 1.86264514923096e-08,
                          "z": -0.0750000029802322
                      },
                      "rotation": {
                          "rx": 3.09492952510482e-06,
                          "ry": -1.33402139113059e-07,
                          "rz": -3.60297195520936e-15
                      }
                  }, {
                      "type": "box",
                      "scale": {
                          "x": 0.279999971389771,
                          "y": 0.026600006967783,
                          "z": 0.150000005960464
                      },
                      "position": {
                          "x": -1.28435203805566e-07,
                          "y": -0.189999714493752,
                          "z": 2.74212652584538e-09
                      },
                      "rotation": {
                          "rx": -2.66804267567977e-08,
                          "ry": -8.004128204675e-08,
                          "rz": 1.86360632178257e-17
                      }
                  }, {
                      "type": "box",
                      "scale": {
                          "x": 0.279999971389771,
                          "y": 0.026600006967783,
                          "z": 0.150000005960464
                      },
                      "position": {
                          "x": -2.29163561016321e-07,
                          "y": 0.189999759197235,
                          "z": 2.57432475336827e-09
                      },
                      "rotation": {
                          "rx": -2.66804267567977e-08,
                          "ry": -8.004128204675e-08,
                          "rz": 1.86360632178257e-17
                      }
                  }, {
                      "type": "box",
                      "scale": {
                          "x": 0.01959996111691,
                          "y": 0.38000026345253,
                          "z": 0.150000005960464
                      },
                      "position": {
                          "x": 0.139999747276306,
                          "y": 2.98023223876953e-08,
                          "z": -8.14907252788544e-09
                      },
                      "rotation": {
                          "rx": -2.66804267567977e-08,
                          "ry": -8.004128204675e-08,
                          "rz": 1.86360632178257e-17
                      }
                  }, {
                      "type": "box",
                      "scale": {
                          "x": 0.01959996111691,
                          "y": 0.38000026345253,
                          "z": 0.150000005960464
                      },
                      "position": {
                          "x": -0.14000016450882,
                          "y": -1.49011611938477e-07,
                          "z": 1.35041773319244e-08
                      },
                      "rotation": {
                          "rx": -2.66804267567977e-08,
                          "ry": -8.004128204675e-08,
                          "rz": 1.86360632178257e-17
                      }
                  }]
              }
          }
      }, {
          "deviceName": "BackWall",
          "deviceType": "object",
          "parameters": {
              "geometry": {
                  "type": "box",
                  "scale": {
                      "x": 0.402099996805191,
                      "y": 1.09560000896454,
                      "z": 0.384005457162857
                  },
                  "position": {
                      "x": -0.0125041902065277,
                      "y": -0.339036643505096,
                      "z": -0.327061951160431
                  },
                  "rotation": {
                      "rx": 1.40236032009125,
                      "ry": 178.743865966797,
                      "rz": 89.5841064453125
                  }
              }
          }
      }, {
          "deviceName": "MiddleWall",
          "deviceType": "object",
          "parameters": {
              "geometry": {
                  "type": "box",
                  "scale": {
                      "x": 0.0953999981284142,
                      "y": 0.546099960803986,
                      "z": 0.165720582008362
                  },
                  "position": {
                      "x": 0.00154566764831543,
                      "y": -0.634920835494995,
                      "z": -0.188080310821533
                  },
                  "rotation": {
                      "rx": 0.34102737903595,
                      "ry": 358.800018310547,
                      "rz": 0.214178040623665
                  }
              }
          }
      }, {
          "deviceName": "FrontWall",
          "deviceType": "object",
          "parameters": {
              "geometry": {
                  "type": "box",
                  "scale": {
                      "x": 0.920000016689301,
                      "y": 0.150000005960464,
                      "z": 0.25
                  },
                  "position": {
                      "x": 0.00999367237091064,
                      "y": -0.936263203620911,
                      "z": -0.239454075694084
                  },
                  "rotation": {
                      "rx": 356.611907958984,
                      "ry": 0.0501468628644943,
                      "rz": 2.0195591787342e-05
                  }
              }
          }
      }, {
          "deviceName": "LeftBox",
          "deviceType": "interactable",
          "parameters": {
              "geometry": {
                  "type": "box",
                  "scale": {
                      "x": 0.379999995231628,
                      "y": 0.259999990463257,
                      "z": 0.200000002980232
                  },
                  "position": {
                      "x": -0.246944084763527,
                      "y": -0.705296516418457,
                      "z": -0.168291628360748
                  },
                  "rotation": {
                      "rx": 0,
                      "ry": 0,
                      "rz": 0
                  }
              }
          }
      }, {
          "deviceName": "RightBox",
          "deviceType": "interactable",
          "parameters": {
              "geometry": {
                  "type": "box",
                  "scale": {
                      "x": 0.370000004768372,
                      "y": 0.300000011920929,
                      "z": 0.200000002980232
                  },
                  "position": {
                      "x": 0.254177570343018,
                      "y": -0.711709439754486,
                      "z": -0.174813330173492
                  },
                  "rotation": {
                      "rx": 1.66752667229986e-09,
                      "ry": 359.650207519531,
                      "rz": 358.763885498047
                  }
              }
          }
      }],
      "version": 20200213
  }

  geometry_json: str = json.dumps(devices_dict)

  settings_engine_dict: Dict[str, Any] = {
      "created": "2020-09-17T22:36:04Z",
      "createdBy": "testusertestusertestusertest",
      "geometry": geometry_json,
      "version": 20200213,
  }
  return json.dumps(settings_engine_dict)


def get_workcell_io_json() -> str:
  """Return a test workcell_io.json."""
  workcell_io = {
      "Proto": ("ChoKBnZhY3V1bRoCdXIoAjoKEghzdGFuZGFyZAodCgdibG93b2ZmGgJ1cigC"
                "OgwSCHN0YW5kYXJkIAEKSwoNdmFjb2ZmLWJsb3dvbhoCdXIoAjABOhgKCnZh"
                "Y3V1bS1vZmYSCHN0YW5kYXJkGAE6GAoKYmxvd29mZi1vbhIIc3RhbmRhcmQg"
                "AQolCg92YWN1dW0tcHJlc3N1cmUaAnVyKAE6DBIIc3RhbmRhcmQgAwogCgx2"
                "YWN1dW0tZ2F1Z2UaAnVyKAM6ChIIc3RhbmRhcmQSCHN0YW5kYXJkEgxjb25m"
                "aWd1cmFibGUSBHRvb2waDgoIc3RhbmRhcmQQASAHGg4KCHN0YW5kYXJkEAIg"
                "BxoSCgxjb25maWd1cmFibGUQASAHGhIKDGNvbmZpZ3VyYWJsZRACIAcaDgoI"
                "c3RhbmRhcmQQAyABGg4KCHN0YW5kYXJkEAQgARoKCgR0b29sEAEgARoKCgR0"
                "b29sEAIgARoKCgR0b29sEAMgASIhChp2YWN1dW0tZ2F1Z2UtbWluLXRocmVz"
                "aG9sZB0AAPpEIhwKFXF1YWxpdHktbWluLXRocmVzaG9sZB0zMzM/IiIKG3Nl"
                "bnNvci1oZWFsdGgtbWluLXRocmVzaG9sZB0zMzM/"),
      "created": "2020-08-27T22:50:32.513053Z",
      "createdBy": "Z2qqLaQ3WVckV8IClWGwuEWOckD2"
  }
  return json.dumps(workcell_io)
