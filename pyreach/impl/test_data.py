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
from typing import Any, Dict, Tuple


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


def get_test_actions() -> Tuple[Tuple[Dict[str, Any], Dict[
    str, Any], str, Tuple[Dict[str, Any], ...], Dict[str, Any]], ...]:
  """Get a series of test case actions and outputs."""
  singulation_actions = [{
      "_steps": [{
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.055156707763671878,
              "y": 0.27040863037109377,
              "z": -0.5407191514968872
          },
          "rot": {
              "x": -0.11628195643424988,
              "y": 0.35665833950042727,
              "z": 0.9268107414245606,
              "w": -0.017183253541588784
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.31074655055999758,
              "y": 0.2453058362007141,
              "z": -0.5561693906784058
          },
          "rot": {
              "x": -0.11852070689201355,
              "y": 0.39984798431396487,
              "z": 0.9081674814224243,
              "w": -0.036141712218523028
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.09024572372436524,
              "y": 0.26927560567855837,
              "z": -0.5438264012336731
          },
          "rot": {
              "x": 0.0014564108569175006,
              "y": 0.46564555168151858,
              "z": 0.8764905333518982,
              "w": -0.1222148984670639
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.1883232593536377,
              "y": 0.24803876876831056,
              "z": -0.556236982345581
          },
          "rot": {
              "x": -0.02783861570060253,
              "y": 0.4526783227920532,
              "z": 0.8493354916572571,
              "w": -0.27006784081459048
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.137556791305542,
              "y": 0.2228027582168579,
              "z": -0.6603227257728577
          },
          "rot": {
              "x": -0.2338070124387741,
              "y": 0.24998824298381806,
              "z": 0.8546422719955444,
              "w": -0.39041873812675478
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.02150106430053711,
              "y": 0.33569109439849856,
              "z": -0.639304518699646
          },
          "rot": {
              "x": 0.020983664318919183,
              "y": 0.27115345001220705,
              "z": 0.9619189500808716,
              "w": -0.02734074927866459
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.20204555988311768,
              "y": 0.3192251920700073,
              "z": -0.7481116652488709
          },
          "rot": {
              "x": 0.15011605620384217,
              "y": 0.14176903665065766,
              "z": 0.9214536547660828,
              "w": 0.32907429337501528
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.17734229564666749,
              "y": 0.31349778175354006,
              "z": -0.6484332084655762
          },
          "rot": {
              "x": 0.32440489530563357,
              "y": 0.16082245111465455,
              "z": 0.855556845664978,
              "w": 0.37002721428871157
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.06824016571044922,
              "y": 0.34116923809051516,
              "z": -0.5412105321884155
          },
          "rot": {
              "x": 0.263325035572052,
              "y": 0.3091835081577301,
              "z": 0.8525419235229492,
              "w": 0.32899510860443118
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.07199680805206299,
              "y": 0.3234095573425293,
              "z": -0.500237762928009
          },
          "rot": {
              "x": 0.04819842055439949,
              "y": 0.48600322008132937,
              "z": 0.8724339604377747,
              "w": 0.018354417756199838
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.08173477649688721,
              "y": 0.3319023847579956,
              "z": -0.5488678216934204
          },
          "rot": {
              "x": 0.3119683563709259,
              "y": 0.4293849468231201,
              "z": 0.8474279046058655,
              "w": 0.013053130358457566
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.08409905433654785,
              "y": 0.27482062578201296,
              "z": -0.4851151406764984
          },
          "rot": {
              "x": -0.16035090386867524,
              "y": 0.3901900351047516,
              "z": 0.8726946711540222,
              "w": -0.24585236608982087
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.16621875762939454,
              "y": 0.2913582921028137,
              "z": -0.595568835735321
          },
          "rot": {
              "x": 0.17923307418823243,
              "y": 0.42937320470809939,
              "z": 0.8569718599319458,
              "w": -0.22161543369293214
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.055191993713378909,
              "y": 0.3450812101364136,
              "z": -0.6489378809928894
          },
          "rot": {
              "x": 0.06677353382110596,
              "y": 0.3458213806152344,
              "z": 0.9288498163223267,
              "w": -0.11483451724052429
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.12487900257110596,
              "y": 0.3032267093658447,
              "z": -0.6225184202194214
          },
          "rot": {
              "x": -0.22458617389202119,
              "y": 0.38407206535339358,
              "z": 0.8889716863632202,
              "w": -0.1085314154624939
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.23992621898651124,
              "y": 0.30920612812042239,
              "z": -0.4970511496067047
          },
          "rot": {
              "x": -0.46570122241973879,
              "y": 0.3053218126296997,
              "z": 0.8140125274658203,
              "w": -0.16518068313598634
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.016614437103271486,
              "y": 0.2758892774581909,
              "z": -0.5372304916381836
          },
          "rot": {
              "x": -0.09272008389234543,
              "y": 0.49821940064430239,
              "z": 0.8580464124679565,
              "w": -0.08328774571418762
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.12767696380615235,
              "y": 0.32739776372909548,
              "z": -0.7407230138778687
          },
          "rot": {
              "x": -0.1105615645647049,
              "y": 0.15697912871837617,
              "z": 0.9473087787628174,
              "w": -0.25639763474464419
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.00080108642578125,
              "y": 0.3821737766265869,
              "z": -0.5630264282226563
          },
          "rot": {
              "x": 0.02442082017660141,
              "y": 0.21607095003128053,
              "z": 0.9760617613792419,
              "w": 0.0045214151032269
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.18361878395080567,
              "y": 0.32750993967056277,
              "z": -0.699981153011322
          },
          "rot": {
              "x": -0.026064973324537278,
              "y": 0.22241060435771943,
              "z": 0.9745050072669983,
              "w": 0.013933375477790833
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }],
      "Preconditions": [],
      "TIPInputs": [],
      "Name": "FixedCalibration",
      "Softstart": False,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "_maxAccel": 0.20000000298023225,
      "_maxVelocity": 0.20000000298023225,
      "_cyclic": True,
      "_intent": "other",
      "_successType": "other",
      "_captureDepthBehavior": "none",
      "_loop": False,
      "_useStepsAsIKHints": False
  }, {
      "_steps": [{
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.1519210934638977,
              "y": 0.18576905131340028,
              "z": 10.898890495300293
          },
          "rot": {
              "x": 0.0,
              "y": -5.587935447692871e-9,
              "z": 3.725290298461914e-9,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.05000000074505806,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": True,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.1519210934638977,
              "y": 0.18576905131340028,
              "z": 10.898890495300293
          },
          "rot": {
              "x": 0.0,
              "y": -5.587935447692871e-9,
              "z": 3.725290298461914e-9,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.05000000074505806,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": True,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": -0.000012976071047887672,
              "y": 0.00002347456211282406,
              "z": 0.000020647439669119194
          },
          "rot": {
              "x": 0.0,
              "y": -2.421438694000244e-8,
              "z": 7.82310962677002e-8,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 1.0,
          "_acceleration": 4.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": True,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": -0.000012976071047887672,
              "y": 0.00002347456211282406,
              "z": 0.000020647439669119194
          },
          "rot": {
              "x": 0.0,
              "y": -2.421438694000244e-8,
              "z": 7.82310962677002e-8,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 1.0,
          "_acceleration": 4.0,
          "_wait": 0.10000000149011612,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": True,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.15738146007061006,
              "y": 0.1924455165863037,
              "z": 11.290617942810059
          },
          "rot": {
              "x": 0.0,
              "y": -5.587935447692871e-9,
              "z": 3.725290298461914e-9,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 1.0,
          "_acceleration": 4.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": True,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.013151168823242188,
              "y": 0.1529741883277893,
              "z": -0.6136350631713867
          },
          "rot": {
              "x": -0.01839587651193142,
              "y": -0.004711020737886429,
              "z": 0.999742865562439,
              "w": -0.012394964694976807
          },
          "_delay": 0.0,
          "_radius": 0.019999999552965165,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.2619915008544922,
              "y": 0.08218997716903687,
              "z": -0.6369067430496216
          },
          "rot": {
              "x": -0.012337777763605118,
              "y": -0.031964052468538287,
              "z": 0.9993637800216675,
              "w": 0.009908456355333329
          },
          "_delay": 0.0,
          "_radius": 0.009999999776482582,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacoff-blowon",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": True,
          "_randomizedOffsetRadiusCM": 6.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.2619915008544922,
              "y": 0.08218997716903687,
              "z": -0.6369067430496216
          },
          "rot": {
              "x": -0.012337776832282544,
              "y": -0.031964052468538287,
              "z": 0.9993637800216675,
              "w": 0.009908461943268776
          },
          "_delay": 0.0,
          "_radius": 0.029999999329447748,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacoff-blowon",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": True,
          "_randomizedOffsetRadiusCM": 6.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.2619915008544922,
              "y": 0.08218997716903687,
              "z": -0.6369067430496216
          },
          "rot": {
              "x": -0.012337777763605118,
              "y": -0.031964052468538287,
              "z": 0.9993637800216675,
              "w": 0.009908460080623627
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.10000000149011612,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacoff-blowon",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": True,
          "_randomizedOffsetRadiusCM": 6.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.03844594955444336,
              "y": 0.16870594024658204,
              "z": -0.5015764236450195
          },
          "rot": {
              "x": -0.01261720061302185,
              "y": -0.031854793429374698,
              "z": 0.9992386698722839,
              "w": 0.018659118562936784
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "blowoff",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.03844594955444336,
              "y": 0.16870594024658204,
              "z": -0.5015764236450195
          },
          "rot": {
              "x": -0.01261720061302185,
              "y": -0.031854793429374698,
              "z": 0.9992386698722839,
              "w": 0.018659118562936784
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "",
          "_setCapabilityType": "blowoff",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }],
      "Preconditions": [],
      "TIPInputs": [{
          "Name": "Torus0",
          "TIPObjectType": "Torus",
          "ChangeMouseRayCastOptions": False,
          "rayCastOptions": {
              "positionFrom": 0,
              "directionFrom": 0,
              "mixDirection": 0,
              "scrollWheelFunction": 0,
              "mixPercentage": 0.0
          },
          "PickData": {
              "label": "",
              "depthTS": 0,
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
                  "x": 0.0,
                  "y": 0.0,
                  "z": 0.0,
                  "w": 0.0
              },
              "tags": [],
              "userTS": 0,
              "deviceType": "",
              "deviceName": ""
          },
          "Dimensions": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
          "TIPPos": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "TIPRot": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0,
              "w": 1.0
          },
          "LocalGOPos": {
              "x": -0.1980351209640503,
              "y": -0.1331457793712616,
              "z": -0.6422970294952393
          },
          "LocalGORot": {
              "x": -0.7008927464485169,
              "y": -0.025330642238259317,
              "z": -0.015135188587009907,
              "w": 0.7126560807228088
          }
      }],
      "Name": "SingulateLeftBin",
      "Softstart": False,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "_maxAccel": 8.0,
      "_maxVelocity": 2.0,
      "_cyclic": False,
      "_intent": "pick",
      "_successType": "vacuum-pressure-sensor",
      "_captureDepthBehavior": "none",
      "_loop": False,
      "_useStepsAsIKHints": False
  }, {
      "_steps": [{
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.4269807040691376,
              "y": -0.33991485834121706,
              "z": 12.915253639221192
          },
          "rot": {
              "x": 4.172325134277344e-7,
              "y": 3.259629011154175e-9,
              "z": -3.3527612686157229e-8,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.05000000074505806,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": True,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.4269801676273346,
              "y": -0.33991485834121706,
              "z": 12.91523551940918
          },
          "rot": {
              "x": 2.3841860752327195e-7,
              "y": -2.0954760149294317e-9,
              "z": -1.885928391232028e-8,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.05000000074505806,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": True,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.00007486135291401297,
              "y": 0.0001776133431121707,
              "z": -0.00001271480414288817
          },
          "rot": {
              "x": 4.172325134277344e-7,
              "y": 4.889443516731262e-9,
              "z": 2.8405338525772097e-7,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 1.0,
          "_acceleration": 4.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": True,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.00007486135291401297,
              "y": 0.0001776133431121707,
              "z": -0.00001271480414288817
          },
          "rot": {
              "x": 4.172325134277344e-7,
              "y": 4.889443516731262e-9,
              "z": 2.8405338525772097e-7,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 1.0,
          "_acceleration": 4.0,
          "_wait": 0.10000000149011612,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": True,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.5047120451927185,
              "y": -0.4017964005470276,
              "z": 15.266460418701172
          },
          "rot": {
              "x": 8.940696716308594e-8,
              "y": 2.3283064365386965e-10,
              "z": -6.28642737865448e-9,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 1.0,
          "_acceleration": 4.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": True,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.013564825057983399,
              "y": 0.18092399835586549,
              "z": -0.654334306716919
          },
          "rot": {
              "x": 0.02751312218606472,
              "y": 0.0007397204171866179,
              "z": 0.9994399547576904,
              "w": 0.019034869968891145
          },
          "_delay": 0.0,
          "_radius": 0.019999999552965165,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.26281678676605227,
              "y": 0.07534366846084595,
              "z": -0.6445802450180054
          },
          "rot": {
              "x": -0.035722892731428149,
              "y": -0.04024830088019371,
              "z": 0.9984188079833984,
              "w": 0.016242941841483117
          },
          "_delay": 0.0,
          "_radius": 0.009999999776482582,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacoff-blowon",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": True,
          "_randomizedOffsetRadiusCM": 6.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.26281678676605227,
              "y": 0.07534366846084595,
              "z": -0.6445802450180054
          },
          "rot": {
              "x": -0.03572288900613785,
              "y": -0.04024829715490341,
              "z": 0.9984188675880432,
              "w": 0.016242943704128267
          },
          "_delay": 0.0,
          "_radius": 0.029999999329447748,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacoff-blowon",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": True,
          "_randomizedOffsetRadiusCM": 6.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.26281678676605227,
              "y": 0.07534366846084595,
              "z": -0.6445802450180054
          },
          "rot": {
              "x": -0.035722892731428149,
              "y": -0.04024830088019371,
              "z": 0.9984188079833984,
              "w": 0.016242941841483117
          },
          "_delay": 0.0,
          "_radius": 0.009999999776482582,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.10000000149011612,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacoff-blowon",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": True,
          "_randomizedOffsetRadiusCM": 6.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.0024805068969726564,
              "y": 0.1664791703224182,
              "z": -0.5675230622291565
          },
          "rot": {
              "x": -0.04089435935020447,
              "y": -0.005485633388161659,
              "z": 0.9988147020339966,
              "w": 0.025822922587394716
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "blowoff",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.0024805068969726564,
              "y": 0.1664791703224182,
              "z": -0.5675230622291565
          },
          "rot": {
              "x": -0.04089435935020447,
              "y": -0.005485633388161659,
              "z": 0.9988147020339966,
              "w": 0.025822922587394716
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": True,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "",
          "_setCapabilityType": "blowoff",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }],
      "Preconditions": [{
          "_preconditionType": 0,
          "_digitalIONumber": 0,
          "_digitalIOValue": False,
          "_maxDigitalIONumber": 9
      }],
      "TIPInputs": [{
          "Name": "Torus0",
          "TIPObjectType": "Torus",
          "ChangeMouseRayCastOptions": False,
          "rayCastOptions": {
              "positionFrom": 0,
              "directionFrom": 0,
              "mixDirection": 0,
              "scrollWheelFunction": 0,
              "mixPercentage": 0.0
          },
          "PickData": {
              "label": "",
              "depthTS": 0,
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
                  "x": 0.0,
                  "y": 0.0,
                  "z": 0.0,
                  "w": 0.0
              },
              "tags": [],
              "userTS": 0,
              "deviceType": "",
              "deviceName": ""
          },
          "Dimensions": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
          "TIPPos": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "TIPRot": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0,
              "w": 1.0
          },
          "LocalGOPos": {
              "x": 0.215956449508667,
              "y": -0.13462474942207337,
              "z": -0.7082916498184204
          },
          "LocalGORot": {
              "x": -0.7160830497741699,
              "y": -0.004250542260706425,
              "z": 0.019307635724544526,
              "w": 0.6977351307868958
          }
      }],
      "Name": "SingulateRightBin",
      "Softstart": False,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "_maxAccel": 8.0,
      "_maxVelocity": 2.0,
      "_cyclic": False,
      "_intent": "pick",
      "_successType": "vacuum-pressure-sensor",
      "_captureDepthBehavior": "none",
      "_loop": False,
      "_useStepsAsIKHints": False
  }, {
      "_steps": [{
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.10489892959594727,
              "y": 0.23676621913909913,
              "z": -0.3586924076080322
          },
          "rot": {
              "x": 0.0000596978425164707,
              "y": 0.00005684150164597668,
              "z": 0.9999991655349731,
              "w": 0.0013059101765975357
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.10490000247955322,
              "y": 0.28263533115386965,
              "z": -0.28039950132369997
          },
          "rot": {
              "x": 1.0865025545925278e-9,
              "y": -4.749253516506268e-17,
              "z": 1.0,
              "w": -4.371138828673793e-8
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.10490000247955322,
              "y": 0.17086505889892579,
              "z": -0.28039950132369997
          },
          "rot": {
              "x": 1.0865025545925278e-9,
              "y": -4.749253516506268e-17,
              "z": 1.0,
              "w": -4.371138828673793e-8
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.10490000247955322,
              "y": 0.17086505889892579,
              "z": -0.3569999933242798
          },
          "rot": {
              "x": 1.0865025545925278e-9,
              "y": -4.749253516506268e-17,
              "z": 1.0,
              "w": -4.371138828673793e-8
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.10490000247955322,
              "y": 0.24087250232696534,
              "z": -0.3569999933242798
          },
          "rot": {
              "x": 1.0865025545925278e-9,
              "y": -4.749253516506268e-17,
              "z": 1.0,
              "w": -4.371138828673793e-8
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": 0,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }],
      "Preconditions": [],
      "TIPInputs": [],
      "Name": "StowSuction1",
      "Softstart": True,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "_maxAccel": 0.20000000298023225,
      "_maxVelocity": 0.20000000298023225,
      "_cyclic": False,
      "_intent": "other",
      "_successType": "other",
      "_captureDepthBehavior": "none",
      "_loop": False,
      "_useStepsAsIKHints": False
  }]

  singulation_actionset = {
      "actions": json.dumps(singulation_actions),
      "created": "2022-02-07T22:58:49.067303Z",
      "createdBy": "HqvtDrvkLweVULubbccjha6QkNX2",
      "version": 7
  }

  singulation_calibration = {
      "devices": [{
          "deviceName": "",
          "deviceType": "color-camera",
          "parameters": {
              "distortion": [
                  -0.27080469727908946, 0.11056397080646445,
                  -0.002888175208016337, 0.0022176524592808266,
                  -0.03963761280368321
              ],
              "extrinsics": [
                  -0.13352896863776986, -0.7593076768386195, 0.58593258600667,
                  -3.094914148957632, -0.00826632718378682, -0.349266716781802
              ],
              "extrinsicsResidual": 0,
              "height": 576,
              "intrinsics": [
                  713.2790103135361, 711.8764384571541, 511.1345716846568,
                  274.0031060178687
              ],
              "intrinsicsResidual": 0.5935269285177991,
              "lensModel": "pinhole",
              "width": 1024
          }
      }, {
          "deviceName": "",
          "deviceType": "depth-camera",
          "parameters": {
              "distortion": [
                  0.09296782765539079, -0.07122572988376769,
                  -0.0033988698499815397, 0.00034412192584354394,
                  0.03408674378026397
              ],
              "distortionDepth": [
                  1.4223016492906035e-11, 0.00010002891458184663, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0
              ],
              "extrinsics": [
                  0.019502533015082455, -0.8177183661767904, 0.5500966529863881,
                  -3.069025520764245, 0.0038246139574653897,
                  0.004698976828941178
              ],
              "extrinsicsResidual": 43.57677009566569,
              "height": 720,
              "intrinsics": [
                  621.968276532595, 621.6601474068248, 638.5769640930959,
                  365.29381662577305
              ],
              "intrinsicsResidual": 0.8865457153547,
              "lensModel": "pinhole",
              "width": 1280
          }
      }, {
          "deviceName": "bodyTag.robot",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  0.0019563297498943677, -0.05774205949350029,
                  0.10066821817803588, 1.2250046390486111, 1.2036767924628018,
                  -1.21924362541116
              ],
              "extrinsicsResidual": 1.4496176547019617,
              "id": 100,
              "intrinsics": [0.04095, 0.04095, 0],
              "linkName": "wrist_2_link",
              "toolMount": "robot"
          }
      }, {
          "deviceName": "tip0.robot",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  0.00698964484035969, -0.0579428747296333, 0.160675629973412,
                  0, 0, 0
              ],
              "intrinsics": [0.04, 0.04, 0.001],
              "subType": "tip",
              "toolMount": "robot"
          }
      }, {
          "deviceName": "tip0.robot.adjust",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  0, 0, 0, -0.0532716661691666, -0.00900643318891525,
                  0.0777493938803673
              ],
              "intrinsics": [0.04, 0.04, 0.001],
              "subType": "tip",
              "toolMount": "tip0.robot"
          }
      }, {
          "deviceName": "",
          "deviceType": "robot",
          "parameters": {
              "calibrationAction": [[
                  1.56049239635468, -1.47792708873749, 1.64017152786255,
                  -1.97951197624207, 4.39641571044922, 0.0125926649197936
              ],
                                    [
                                        1.37298917770386, -1.10473425806079,
                                        1.4450801054584, -0.856238679294922,
                                        4.59058809280396, -0.342052284871237
                                    ],
                                    [
                                        1.65098524093628, -0.614583329563477,
                                        1.11074525514712, -1.87809052089834,
                                        5.67157077789307, -0.117683235798971
                                    ],
                                    [
                                        1.46918535232544, -0.627487019901611,
                                        1.12028772035708, -1.87159885982656,
                                        5.57706308364868, -0.110883537922994
                                    ],
                                    [
                                        1.26110887527466, -0.680742577915527,
                                        1.11452943483462, -2.0089069805541,
                                        5.3484034538269, -0.11096698442568
                                    ],
                                    [
                                        1.34934568405151, -0.77960284173999,
                                        1.11379892030825, -2.05016865352773,
                                        4.88609027862549, -0.111003224049703
                                    ],
                                    [
                                        1.34936952590942, -0.588884190922119,
                                        1.11354715028872, -2.39272179226064,
                                        4.88628196716309, -0.11096698442568
                                    ],
                                    [
                                        1.34934568405151, -0.542744950657227,
                                        1.11354715028872, -2.46851839641714,
                                        5.16252136230469, -0.110907379780905
                                    ],
                                    [
                                        1.2458086013794, -0.588991956119873,
                                        1.11371499696841, -2.33742775539541,
                                        5.16192245483398, -0.111015144978659
                                    ],
                                    [
                                        1.2458324432373, -0.588968114261963,
                                        1.1137264410602, -2.3374039135375,
                                        5.16192245483398, -0.111038509999411
                                    ],
                                    [
                                        1.24621629714966, -0.588836507206299,
                                        1.1008680502521, -2.35439409832143,
                                        4.5960054397583, -0.111086670552389
                                    ],
                                    [
                                        1.32447004318237, -0.620460824375488,
                                        1.10163385072817, -2.29903282741689,
                                        3.91244649887085, -0.111146275197164
                                    ],
                                    [
                                        1.48494672775269, -0.615744428043701,
                                        1.1042802969562, -2.20900978664541,
                                        3.91207504272461, -0.11094314256777
                                    ],
                                    [
                                        1.62332153320313, -0.615876035099365,
                                        1.10390931764712, -2.20912994960927,
                                        3.91231465339661, -0.110955063496725
                                    ],
                                    [
                                        1.66471338272095, -0.616020039921143,
                                        1.10376531282534, -2.20932116130971,
                                        4.19493532180786, -0.110907379780905
                                    ],
                                    [
                                        1.68844604492188, -0.589087800388672,
                                        1.10370523134341, -2.47179379085683,
                                        4.42288112640381, -0.11089545885195
                                    ],
                                    [
                                        1.63367700576782, -0.734720544224121,
                                        1.2843020598041, -2.55852665523672,
                                        4.42284488677979, -0.110835854207174
                                    ],
                                    [
                                        1.48879432678223, -0.803047494297363,
                                        1.40239936510195, -2.55843128780508,
                                        4.87858152389526, -0.11094314256777
                                    ],
                                    [
                                        1.28805494308472, -0.83502562463794,
                                        1.51362640062441, -2.38780035595083,
                                        5.36272811889648, -0.214556519185201
                                    ],
                                    [
                                        1.24613237380981, -0.928122357731201,
                                        1.51003867784609, -1.72991718868398,
                                        5.34205532073975, -0.214604202901022
                                    ],
                                    [
                                        1.20238351821899, -0.957451657657959,
                                        1.50911552110781, -1.5496462148479,
                                        5.22432804107666, -0.214639965687887
                                    ],
                                    [
                                        1.27244329452515, -0.971557931309082,
                                        1.40765220323671, -1.22933657587085,
                                        4.72044515609741, -0.578144375477926
                                    ],
                                    [
                                        1.28503847122192, -0.962676839237549,
                                        1.40680343309511, -1.32523806512866,
                                        4.31265878677368, -0.638865772877828
                                    ],
                                    [
                                        1.35605335235596, -0.876940087681152,
                                        1.27321273485293, -1.32552607477222,
                                        4.09133863449097, -0.784958187733785
                                    ],
                                    [
                                        1.46415138244629, -0.703559712772705,
                                        1.09053498903383, -1.50189764917407,
                                        3.89107990264893, -0.94761306444277
                                    ],
                                    [
                                        1.57111406326294, -0.740511731510498,
                                        1.09078675905337, -1.7949177227416,
                                        4.13260889053345, -0.94763690630068
                                    ]],
              "calibrationPose": {
                  "cartesian": [
                      -0.00914872029417805, -0.511452807569245,
                      0.238648395478641, 0.100927971334481, -3.04464438924935,
                      0.642038543258026
                  ],
                  "joints": [
                      1.2659969329834, -1.35129006326709, 2.17243224779238,
                      -2.79491867641591, 4.82020664215088, -0.349030319844381
                  ]
              },
              "extrinsics": [0, 0, 0, 0, 0, 0],
              "extrinsicsResidual": 1.4496176547019617,
              "urdf": "ur5e.urdf"
          }
      }],
      "robot-name": "BD8ED1",
      "timestamp": 1633547978.999653,
      "version": 20190118
  }

  actions = [{
      "_steps": [{
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.10880321264266968,
              "y": 0.3553914427757263,
              "z": -0.34069526195526125,
          },
          "rot": {
              "x": 0.2976646423339844,
              "y": -0.05556989088654518,
              "z": 0.9490106701850891,
              "w": 0.0876726433634758
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": "",
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.31074655055999758,
              "y": 0.2453058362007141,
              "z": -0.5561693906784058
          },
          "rot": {
              "x": -0.11852070689201355,
              "y": 0.39984798431396487,
              "z": 0.9081674814224243,
              "w": -0.036141712218523028
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.09024572372436524,
              "y": 0.26927560567855837,
              "z": -0.5438264012336731
          },
          "rot": {
              "x": 0.0014564108569175006,
              "y": 0.46564555168151858,
              "z": 0.8764905333518982,
              "w": -0.1222148984670639
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.1883232593536377,
              "y": 0.24803876876831056,
              "z": -0.556236982345581
          },
          "rot": {
              "x": -0.02783861570060253,
              "y": 0.4526783227920532,
              "z": 0.8493354916572571,
              "w": -0.27006784081459048
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.137556791305542,
              "y": 0.2228027582168579,
              "z": -0.6603227257728577
          },
          "rot": {
              "x": -0.2338070124387741,
              "y": 0.24998824298381806,
              "z": 0.8546422719955444,
              "w": -0.39041873812675478
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.02150106430053711,
              "y": 0.33569109439849856,
              "z": -0.639304518699646
          },
          "rot": {
              "x": 0.020983664318919183,
              "y": 0.27115345001220705,
              "z": 0.9619189500808716,
              "w": -0.02734074927866459
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.20204555988311768,
              "y": 0.3192251920700073,
              "z": -0.7481116652488709
          },
          "rot": {
              "x": 0.15011605620384217,
              "y": 0.14176903665065766,
              "z": 0.9214536547660828,
              "w": 0.32907429337501528
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.17734229564666749,
              "y": 0.31349778175354006,
              "z": -0.6484332084655762
          },
          "rot": {
              "x": 0.32440489530563357,
              "y": 0.16082245111465455,
              "z": 0.855556845664978,
              "w": 0.37002721428871157
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.06824016571044922,
              "y": 0.34116923809051516,
              "z": -0.5412105321884155
          },
          "rot": {
              "x": 0.263325035572052,
              "y": 0.3091835081577301,
              "z": 0.8525419235229492,
              "w": 0.32899510860443118
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.07199680805206299,
              "y": 0.3234095573425293,
              "z": -0.500237762928009
          },
          "rot": {
              "x": 0.04819842055439949,
              "y": 0.48600322008132937,
              "z": 0.8724339604377747,
              "w": 0.018354417756199838
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.08173477649688721,
              "y": 0.3319023847579956,
              "z": -0.5488678216934204
          },
          "rot": {
              "x": 0.3119683563709259,
              "y": 0.4293849468231201,
              "z": 0.8474279046058655,
              "w": 0.013053130358457566
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.08409905433654785,
              "y": 0.27482062578201296,
              "z": -0.4851151406764984
          },
          "rot": {
              "x": -0.16035090386867524,
              "y": 0.3901900351047516,
              "z": 0.8726946711540222,
              "w": -0.24585236608982087
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.16621875762939454,
              "y": 0.2913582921028137,
              "z": -0.595568835735321
          },
          "rot": {
              "x": 0.17923307418823243,
              "y": 0.42937320470809939,
              "z": 0.8569718599319458,
              "w": -0.22161543369293214
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.055191993713378909,
              "y": 0.3450812101364136,
              "z": -0.6489378809928894
          },
          "rot": {
              "x": 0.06677353382110596,
              "y": 0.3458213806152344,
              "z": 0.9288498163223267,
              "w": -0.11483451724052429
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.12487900257110596,
              "y": 0.3032267093658447,
              "z": -0.6225184202194214
          },
          "rot": {
              "x": -0.22458617389202119,
              "y": 0.38407206535339358,
              "z": 0.8889716863632202,
              "w": -0.1085314154624939
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.23992621898651124,
              "y": 0.30920612812042239,
              "z": -0.4970511496067047
          },
          "rot": {
              "x": -0.46570122241973879,
              "y": 0.3053218126296997,
              "z": 0.8140125274658203,
              "w": -0.16518068313598634
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.016614437103271486,
              "y": 0.2758892774581909,
              "z": -0.5372304916381836
          },
          "rot": {
              "x": -0.09272008389234543,
              "y": 0.49821940064430239,
              "z": 0.8580464124679565,
              "w": -0.08328774571418762
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.12767696380615235,
              "y": 0.32739776372909548,
              "z": -0.7407230138778687
          },
          "rot": {
              "x": -0.1105615645647049,
              "y": 0.15697912871837617,
              "z": 0.9473087787628174,
              "w": -0.25639763474464419
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.00080108642578125,
              "y": 0.3821737766265869,
              "z": -0.5630264282226563
          },
          "rot": {
              "x": 0.02442082017660141,
              "y": 0.21607095003128053,
              "z": 0.9760617613792419,
              "w": 0.0045214151032269
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.18361878395080567,
              "y": 0.32750993967056277,
              "z": -0.699981153011322
          },
          "rot": {
              "x": -0.026064973324537278,
              "y": 0.22241060435771943,
              "z": 0.9745050072669983,
              "w": 0.013933375477790833
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }],
      "Preconditions": [],
      "TIPInputs": [],
      "Name": "FixedCalibration",
      "Softstart": False,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "_maxAccel": 0.20000000298023225,
      "_maxVelocity": 0.20000000298023225,
      "_cyclic": True,
      "_intent": "other",
      "_successType": "other",
      "_captureDepthBehavior": "none",
      "_loop": False,
      "_useStepsAsIKHints": False
  }, {
      "_steps": [{
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.022123483940958978,
              "y": 0.3039575517177582,
              "z": -0.46248671412467959
          },
          "rot": {
              "x": -0.09331396222114563,
              "y": -0.043877530843019488,
              "z": 0.9946368336677551,
              "w": -0.0080562187358737
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 2,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "depth-camera",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": "<autogenerate>"
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.024539798498153688,
              "y": 0.26560112833976748,
              "z": -0.5679639577865601
          },
          "rot": {
              "x": -0.09275462478399277,
              "y": -0.04656444117426872,
              "z": 0.9944149255752564,
              "w": -0.01916499063372612
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.29401108622550967,
              "y": 0.3111284375190735,
              "z": 4.818350791931152
          },
          "rot": {
              "x": -3.874301341966202e-7,
              "y": 7.078050856534901e-8,
              "z": -7.729976658765736e-8,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 1.2219406366348267,
              "y": 1.292945384979248,
              "z": 20.025083541870118
          },
          "rot": {
              "x": 8.94069742685133e-8,
              "y": -9.313226634333205e-9,
              "z": -1.2945385208240624e-7,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.000007074521818140056,
              "y": -4.1251624338656259e-7,
              "z": -0.000006388996553141624
          },
          "rot": {
              "x": -1.7881389169360774e-7,
              "y": 6.146727571376687e-8,
              "z": -7.171182403453713e-8,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.9714557528495789,
              "y": 1.0279104709625245,
              "z": 15.920248985290528
          },
          "rot": {
              "x": 8.94069742685133e-8,
              "y": -1.4156104555240746e-7,
              "z": -1.2107194891086693e-7,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.2640698254108429,
              "y": 0.2719118297100067,
              "z": -0.567962110042572
          },
          "rot": {
              "x": -0.09275461733341217,
              "y": -0.04656441882252693,
              "z": 0.9944149255752564,
              "w": -0.019165076315402986
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 1,
          "_parentType": 1,
          "pos": {
              "x": 0.05991702899336815,
              "y": 0.06093187257647514,
              "z": 0.9941903948783875
          },
          "rot": {
              "x": 1.1920930376163597e-7,
              "y": -6.658957119043407e-8,
              "z": 1.3038516932795119e-8,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 1,
          "_parentType": 1,
          "pos": {
              "x": 0.07704883068799973,
              "y": 0.07835384458303452,
              "z": 1.2784546613693238
          },
          "rot": {
              "x": 0.0,
              "y": -1.0710209608078003e-8,
              "z": -9.313225746154786e-10,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.4087449908256531,
              "y": -0.02777138352394104,
              "z": -0.7395716309547424
          },
          "rot": {
              "x": 0.6844152808189392,
              "y": 0.009475883096456528,
              "z": -0.03231767565011978,
              "w": -0.7283141613006592
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.4087449908256531,
              "y": -0.027771413326263429,
              "z": -0.7395716309547424
          },
          "rot": {
              "x": 0.6844152808189392,
              "y": 0.009475872851908207,
              "z": -0.032317690551280978,
              "w": -0.7283141613006592
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.10000000149011612,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 1,
          "_parentType": 1,
          "pos": {
              "x": 0.10945743322372437,
              "y": 0.11129789054393769,
              "z": 1.8158009052276612
          },
          "rot": {
              "x": -1.7881392011531717e-7,
              "y": 1.1362133989223367e-7,
              "z": 4.8428766774577528e-8,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": 0.01747220754623413,
              "y": 0.2605147659778595,
              "z": -0.36826515197753909
          },
          "rot": {
              "x": -0.07766502350568772,
              "y": -0.04519135504961014,
              "z": 0.9957872033119202,
              "w": -0.01826751045882702
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }],
      "Preconditions": [],
      "TIPInputs": [{
          "Name": "Torus0",
          "TIPObjectType": "Torus",
          "ChangeMouseRayCastOptions": True,
          "rayCastOptions": {
              "positionFrom": 0,
              "directionFrom": 0,
              "mixDirection": 2,
              "scrollWheelFunction": 0,
              "mixPercentage": 50.0
          },
          "PickData": {
              "label": "",
              "depthTS": 0,
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
                  "x": 0.0,
                  "y": 0.0,
                  "z": 0.0,
                  "w": 0.0
              },
              "tags": [],
              "userTS": 0,
              "deviceType": "",
              "deviceName": ""
          },
          "Dimensions": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
          "TIPPos": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "TIPRot": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0,
              "w": 1.0
          },
          "LocalGOPos": {
              "x": 0.0427577942609787,
              "y": -0.23438525199890138,
              "z": -0.5861091613769531
          },
          "LocalGORot": {
              "x": 0.6836310029029846,
              "y": 0.020795157179236413,
              "z": -0.022181160748004915,
              "w": -0.7291942834854126
          },
          "InteractableSpaces": []
      }, {
          "Name": "Torus1",
          "TIPObjectType": "Torus",
          "ChangeMouseRayCastOptions": True,
          "rayCastOptions": {
              "positionFrom": 1,
              "directionFrom": 2,
              "mixDirection": 2,
              "scrollWheelFunction": 0,
              "mixPercentage": 0.0
          },
          "PickData": {
              "label": "",
              "depthTS": 0,
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
                  "x": 0.0,
                  "y": 0.0,
                  "z": 0.0,
                  "w": 0.0
              },
              "tags": [],
              "userTS": 0,
              "deviceType": "",
              "deviceName": ""
          },
          "Dimensions": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
          "TIPPos": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "TIPRot": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0,
              "w": 1.0
          },
          "LocalGOPos": {
              "x": 0.4087449908256531,
              "y": -0.043979138135910037,
              "z": -0.7395716905593872
          },
          "LocalGORot": {
              "x": 0.6844152212142944,
              "y": 0.009475848637521267,
              "z": -0.03231772407889366,
              "w": -0.728314220905304
          },
          "InteractableSpaces": []
      }],
      "Name": "FlipAction",
      "Softstart": False,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "_maxAccel": 1.0,
      "_maxVelocity": 1.0,
      "_cyclic": False,
      "_intent": "pick",
      "_successType": "vacuum-pressure-sensor",
      "_captureDepthBehavior": "grab-release",
      "_loop": False,
      "_useStepsAsIKHints": False
  }, {
      "_steps": [{
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.0477999746799469,
              "y": 0.17420050501823426,
              "z": -0.376600444316864
          },
          "rot": {
              "x": 0.01599094085395336,
              "y": 0.02108030393719673,
              "z": -0.9993753433227539,
              "w": -0.023427626118063928
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 2,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "depth-camera",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": "<autogenerate>"
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.04875096678733826,
              "y": 0.3293556869029999,
              "z": -0.5129516124725342
          },
          "rot": {
              "x": -0.03891004994511604,
              "y": 0.01264545600861311,
              "z": 0.9991549849510193,
              "w": 0.0039277770556509499
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": -0.515662431716919,
              "y": 1.2091503143310547,
              "z": 16.514835357666017
          },
          "rot": {
              "x": 0.000003963707968068775,
              "y": -0.000002373940787947504,
              "z": 8.568165412725648e-7,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": -0.026510708034038545,
              "y": 0.0618799589574337,
              "z": 0.8374755382537842
          },
          "rot": {
              "x": 0.000001341104166385776,
              "y": -9.788197985471925e-7,
              "z": 3.948806863718346e-7,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": 0.08200448006391525,
              "y": -0.1929340958595276,
              "z": -2.645184278488159
          },
          "rot": {
              "x": -0.0000036656851989391727,
              "y": 0.0000020898876300634585,
              "z": -5.438923267320206e-7,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.029999999329447748,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 0,
          "_parentType": 1,
          "pos": {
              "x": -0.49322131276130679,
              "y": 1.1563704013824463,
              "z": 15.788209915161133
          },
          "rot": {
              "x": 0.0000056624407989147588,
              "y": -0.0000026077029815496646,
              "z": 6.454064873651078e-7,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.019999999552965165,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 1,
          "_parentType": 1,
          "pos": {
              "x": -0.6029996275901794,
              "y": 1.4167592525482178,
              "z": 21.469608306884767
          },
          "rot": {
              "x": -0.00000122189510420867,
              "y": 2.6542690534370197e-7,
              "z": -7.851048167140107e-7,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.009999999776482582,
          "_velocity": 0.0,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 1,
          "_parentType": 1,
          "pos": {
              "x": -0.12704050540924073,
              "y": 0.2995070219039917,
              "z": 4.529036045074463
          },
          "rot": {
              "x": -9.536742027194123e-7,
              "y": 1.8440184135215532e-7,
              "z": -2.9802318834981635e-8,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.10000000149011612,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": True,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 1,
          "_parentType": 1,
          "pos": {
              "x": -0.09911365061998368,
              "y": 0.23261569440364839,
              "z": 3.5274360179901125
          },
          "rot": {
              "x": 5.960464477539063e-8,
              "y": -1.1175870895385742e-7,
              "z": -8.009374141693115e-8,
              "w": -1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.10000000149011612,
          "_acceleration": 0.20000000298023225,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": True,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "",
          "_setCapabilityType": "vacuum",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "DigitalOutput",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": 1,
          "_parentType": 1,
          "pos": {
              "x": -0.6209169626235962,
              "y": 1.4603257179260255,
              "z": 22.115964889526368
          },
          "rot": {
              "x": -0.00000122189510420867,
              "y": 5.522742299035599e-7,
              "z": -3.837048438981583e-7,
              "w": 1.0
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 1.0,
          "_acceleration": 0.8999999761581421,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": True,
          "_individualVelocityAcceleration": True,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.04687786102294922,
              "y": 0.31915420293807986,
              "z": -0.4877152442932129
          },
          "rot": {
              "x": -0.015996458008885385,
              "y": -0.02110425941646099,
              "z": 0.9993748664855957,
              "w": 0.023422542959451677
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": False,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": False,
          "_setCapabilityName": "",
          "_setCapabilityType": "",
          "_setCapabilityValue": False,
          "_setCapabilityIOType": "",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }, {
          "_tipInputIdx": -1,
          "_parentType": 0,
          "pos": {
              "x": -0.04687786102294922,
              "y": 0.31915420293807986,
              "z": -0.4877152442932129
          },
          "rot": {
              "x": -0.015996458008885385,
              "y": -0.02110425941646099,
              "z": 0.9993748664855957,
              "w": 0.023422542959451677
          },
          "_delay": 0.0,
          "_radius": 0.0,
          "_velocity": 0.0,
          "_acceleration": 0.0,
          "_wait": 0.0,
          "_parentStepIdx": -1,
          "_useProcessMode": False,
          "_individualVelocityAcceleration": False,
          "_useForceMode": False,
          "_useServoJMode": False,
          "_useSkipMove": True,
          "_setDigitalIO": False,
          "_setToolDigitalIO": False,
          "_setDigitalIONumber": 0,
          "_acquireImageMode": 0,
          "_setDigitalIOValue": False,
          "_setToolDigitalIOValue": False,
          "_setCapability": True,
          "_setCapabilityName": "place-point",
          "_setCapabilityType": "point-reached",
          "_setCapabilityValue": True,
          "_setCapabilityIOType": "Event",
          "_randomizedOffset": False,
          "_randomizedOffsetRadiusCM": 5.0,
          "_useTorqueLimits": False,
          "_torqueLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useForceLimits": False,
          "_forceLimitType": "JOINTS",
          "_forceLimits": {
              "maximum": [],
              "minimum": []
          },
          "_useSensorLimits": False,
          "_sensorLimits": [],
          "_rawRobotScript": "",
          "_waitAction": "",
          "_waitAbortMessage": "",
          "_acquireImageTag": ""
      }],
      "Preconditions": [],
      "TIPInputs": [{
          "Name": "Torus0",
          "TIPObjectType": "Torus",
          "ChangeMouseRayCastOptions": True,
          "rayCastOptions": {
              "positionFrom": 0,
              "directionFrom": 2,
              "mixDirection": 0,
              "scrollWheelFunction": 0,
              "mixPercentage": 0.0
          },
          "PickData": {
              "label": "",
              "depthTS": 0,
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
                  "x": 0.0,
                  "y": 0.0,
                  "z": 0.0,
                  "w": 0.0
              },
              "tags": [],
              "userTS": 0,
              "deviceType": "",
              "deviceName": ""
          },
          "Dimensions": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
          "TIPPos": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "TIPRot": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0,
              "w": 1.0
          },
          "LocalGOPos": {
              "x": -0.33309999108314516,
              "y": -0.15219999849796296,
              "z": -0.603600025177002
          },
          "LocalGORot": {
              "x": -0.6807690858840942,
              "y": 0.013688952662050724,
              "z": -0.008510054089128971,
              "w": 0.7323207855224609
          },
          "InteractableSpaces": []
      }, {
          "Name": "Torus1",
          "TIPObjectType": "Torus",
          "ChangeMouseRayCastOptions": True,
          "rayCastOptions": {
              "positionFrom": 0,
              "directionFrom": 2,
              "mixDirection": 0,
              "scrollWheelFunction": 0,
              "mixPercentage": 0.0
          },
          "PickData": {
              "label": "",
              "depthTS": 0,
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
                  "x": 0.0,
                  "y": 0.0,
                  "z": 0.0,
                  "w": 0.0
              },
              "tags": [],
              "userTS": 0,
              "deviceType": "",
              "deviceName": ""
          },
          "Dimensions": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "Padding": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
          "TIPPos": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0
          },
          "TIPRot": {
              "x": 0.0,
              "y": 0.0,
              "z": 0.0,
              "w": 1.0
          },
          "LocalGOPos": {
              "x": 0.13040000200271607,
              "y": -0.22419999539852143,
              "z": -0.5676165819168091
          },
          "LocalGORot": {
              "x": 0.6834219098091126,
              "y": -0.012592224404215813,
              "z": 0.00741222407668829,
              "w": -0.7298774123191834
          },
          "InteractableSpaces": []
      }],
      "Name": "Kit",
      "Softstart": False,
      "SoftstartAccel": 1.0,
      "SoftstartVelocity": 1.0,
      "_maxAccel": 1.2000000476837159,
      "_maxVelocity": 1.7999999523162842,
      "_cyclic": False,
      "_intent": "pick",
      "_successType": "vacuum-pressure-sensor",
      "_captureDepthBehavior": "grab-release",
      "_loop": False,
      "_useStepsAsIKHints": False
  }]

  actionset = {
      "actions": json.dumps(actions),
      "created": "2022-04-20T22:40:44Z",
      "createdBy": "bcCjSacTCCceFOJaK9yHPhAvLQt2",
      "version": 7
  }

  calibration = {
      "devices": [{
          "deviceName": "",
          "deviceType": "color-camera",
          "parameters": {
              "distortion": [
                  -0.232771846103376, -0.00436337539603741,
                  -0.000912035179184453, -0.00214161101400129,
                  0.0445093868474967
              ],
              "extrinsics": [
                  -0.21919568134341372, -0.7633209198699332, 0.5836282202045919,
                  -2.9612602515553985, -0.03885142304025799,
                  -0.20119612201927406
              ],
              "extrinsicsResidual": 0,
              "height": 576,
              "intrinsics": [
                  711.783178713005, 710.270431193363, 506.849883143857,
                  264.374826204481
              ],
              "intrinsicsResidual": 0.836813487392329,
              "lensModel": "pinhole",
              "width": 1024
          }
      }, {
          "deviceName": "",
          "deviceType": "depth-camera",
          "parameters": {
              "distortion": [
                  0.122119607639666, -0.130516242835868, -0.00840815327634313,
                  0.000499561618412576, 0.0734268404541668
              ],
              "distortionDepth": [
                  3.52007638453419e-11, 0.000100225868502833, 0.0, 0.0, 0.0,
                  0.0, 0.0, 0.0
              ],
              "extrinsics": [
                  0.02361304804621918, -0.800648663796076, 0.5603799064649113,
                  -2.7919598537966444, -0.02612430086290207, 0.01512230053971749
              ],
              "extrinsicsResidual": 259.9083399864401,
              "height": 720,
              "intrinsics": [
                  622.912211859472, 622.22743085877, 637.001060104678,
                  351.842089457793
              ],
              "intrinsicsResidual": 0.955089908063061,
              "lensModel": "pinhole",
              "width": 1280
          }
      }, {
          "deviceName": "bodyTag.robot",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  0.00043580862246931165, -0.057938097281557965,
                  0.09753416477876792, 1.1527384879730176, 1.2903740674162891,
                  -1.2874363619366278
              ],
              "extrinsicsResidual": 1.8025671553513074,
              "id": 100,
              "intrinsics": [0.04095, 0.04095, 0],
              "linkName": "wrist_2_link",
              "toolMount": "robot"
          }
      }, {
          "deviceName": "tip.robot",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  0.00445348523808725, -0.055702600244064, 0.162651221347607, 0,
                  0, 0
              ],
              "extrinsicsAdjust": [0, 0, -0.005, 0, 0, 0],
              "intrinsics": [0.04, 0.04, 0.001],
              "subType": "tip",
              "toolMount": "robot"
          }
      }, {
          "deviceName": "tip0.robot",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  -0.000898663762553914, -0.00282612502936733, 0.31690161972863,
                  0, 0, 0
              ],
              "intrinsics": [0.04, 0.04, 0.001],
              "subType": "tip",
              "toolMount": "robot"
          }
      }, {
          "deviceName": "tip0.robot.adjust",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  0.00328632909804583, 0.000418265117332339,
                  -0.00300204753875732, 0.0228533148765564, -0.0173381567001343,
                  0.0402406342327595
              ],
              "intrinsics": [0.04, 0.04, 0.001],
              "subType": "tip",
              "toolMount": "object-tip0.robot"
          }
      }, {
          "deviceName": "",
          "deviceType": "robot",
          "parameters": {
              "calibrationAction": [[
                  0.915253520011902, -1.93296384811401, 2.25403642654419,
                  -2.05777812004089, -1.69678765932192, -0.058153435587883
              ],
                                    [
                                        1.2494148015976, -1.10655696809802,
                                        1.52941781679262, -1.44779189050708,
                                        -2.1045597235309, -0.0586307684527796
                                    ],
                                    [
                                        1.45338714122772, -1.07413165391002,
                                        1.58640176454653, -1.61278118709707,
                                        -1.33827430406679, -0.0586064497577112
                                    ],
                                    [
                                        1.56284463405609, -1.0427041810802,
                                        1.58682138124575, -1.61260141948842,
                                        -2.13274842897524, -0.0586064497577112
                                    ],
                                    [
                                        1.47415459156036, -0.962309555416443,
                                        1.31294042268862, -1.18848522127185,
                                        -1.97674018541445, -0.0591452757464808
                                    ],
                                    [
                                        1.31449353694916, -0.964371399288513,
                                        1.34066278139223, -1.29857976854358,
                                        -1.32411891618838, -0.059157673512594
                                    ],
                                    [
                                        1.30593264102936, -0.809184030895569,
                                        1.12095243135561, -1.93022837261342,
                                        -1.66292268434633, 0.245196342468262
                                    ],
                                    [
                                        1.35090410709381, -0.841424779301025,
                                        1.22714311281313, -1.93050446132802,
                                        -1.20006400743593, 0.245184421539307
                                    ],
                                    [
                                        1.41222846508026, -0.859414176349976,
                                        1.74571878114809, -2.99461092571401,
                                        -1.54183036485781, 0.244968891143799
                                    ],
                                    [
                                        1.62374985218048, -0.803447441463806,
                                        1.66788369814028, -2.95355715374135,
                                        -1.8765929381, 0.287188768386841
                                    ],
                                    [
                                        1.63564670085907, -0.688351110821106,
                                        1.26513749757876, -2.15539326290273,
                                        -2.22517997423281, 0.420763969421387
                                    ],
                                    [
                                        1.73510038852692, -0.917991594677307,
                                        1.64940148988833, -2.32473768810415,
                                        -1.82818967500796, 0.421349763870239
                                    ],
                                    [
                                        1.72785437107086, -1.08592744291339,
                                        1.87429696718325, -1.91738571743154,
                                        -1.4208725134479, 0.421122550964355
                                    ],
                                    [
                                        1.41724169254303, -1.09293539941821,
                                        1.87429696718325, -1.96195854763173,
                                        -2.30853706995119, 0.422234296798706
                                    ],
                                    [
                                        1.47348511219025, -1.19791586816821,
                                        2.02944070497622, -1.93067230800771,
                                        -2.13926250139345, 0.421684503555298
                                    ],
                                    [
                                        1.4747406244278, -1.0531919759563,
                                        1.9230116049396, -2.61780514339589,
                                        -1.83175927797426, 0.422043085098267
                                    ],
                                    [
                                        1.40597069263458, -1.08305950582538,
                                        1.82973748842348, -2.35183586696767,
                                        -1.19282895723452, 0.420716047286987
                                    ],
                                    [
                                        1.33707845211029, -1.10339744508777,
                                        1.58026391664614, -1.81364407161855,
                                        -2.10105592409243, 0.421122550964355
                                    ],
                                    [
                                        1.22633039951324, -1.01731558263812,
                                        1.44789201418032, -1.72708382228994,
                                        -1.49327117601504, 0.396647691726685
                                    ],
                                    [
                                        1.32774889469147, -0.773400620823242,
                                        1.11231547990908, -1.80610909084463,
                                        -1.27612859407534, 0.304186582565308
                                    ],
                                    [
                                        1.39440739154816, -1.06335587919269,
                                        1.55639917055239, -1.90607990841054,
                                        -2.2565110365497, 0.0519585609436035
                                    ],
                                    [
                                        1.58950769901276, -1.07787568986926,
                                        1.55649453798403, -1.44785173357043,
                                        -1.84548598924746, 0.0519347190856934
                                    ],
                                    [
                                        1.10376369953156, -1.07871563852344,
                                        1.55641061464419, -1.31578476846729,
                                        -1.66303044954409, 0.051790714263916
                                    ],
                                    [
                                        1.50302350521088, -0.751890496616699,
                                        1.27902299562563, -0.853224114780762,
                                        -1.29302484193911, -0.766444508229391
                                    ],
                                    [
                                        1.62407290935516, -0.792955951099731,
                                        1.2252872625934, -1.79865803341054,
                                        -1.26547414461245, -0.766468350087301
                                    ],
                                    [
                                        1.45539700984955, -0.782895402317383,
                                        1.10596686998476, -1.87504639248037,
                                        -1.51398784319033, -0.766755406056539
                                    ],
                                    [
                                        1.35642874240875, -1.15459974229846,
                                        1.92745668092837, -1.86143269161367,
                                        -1.6554482618915, -0.615078274403707
                                    ]],
              "calibrationPose": {
                  "cartesian": [
                      0.104070506530713, 0.702342330822366, 0.156736617206672,
                      -3.08323174899601, 0.329285855148894, 0.175471978148736
                  ],
                  "joints": [
                      1.59823513031006, -2.28654827694082, -1.49076557159424,
                      -0.884231404667236, 1.67799806594849, 0.242958545684815
                  ]
              },
              "extrinsics": [0, 0, 0, 0, 0, 0],
              "extrinsicsResidual": 1.8025671553513074,
              "urdf": "ur5e.urdf"
          }
      }, {
          "deviceName": "realsense",
          "deviceType": "color-camera",
          "parameters": {
              "distortion": [0, 0, 0, 0, 0],
              "extrinsics": [0, 0, 0, 0, 0, 0],
              "extrinsicsResidual": 0,
              "height": 480,
              "intrinsics": [600, 600, 320, 240],
              "lensModel": "pinhole",
              "width": 640
          }
      }, {
          "deviceName": "april300",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  -0.08267513607438332, -0.8385150644397315,
                  -0.25941099731222417, 0.14502940552303228,
                  0.17421544724413676, 1.5554908574789494
              ],
              "id": 300,
              "intrinsics": [0.04095, 0.04095, 0]
          }
      }, {
          "deviceName": "april302",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  -0.08844481479739315, -0.27896925939064715,
                  -0.27165557527564627, 0.014251776891578747,
                  0.04653204902664903, -0.012934687157666845
              ],
              "id": 302,
              "intrinsics": [0.04095, 0.04095, 0]
          }
      }, {
          "deviceName": "april303",
          "deviceType": "object",
          "parameters": {
              "extrinsics": [
                  -0.3778923226090352, -0.28735129616807037,
                  -0.26352561203198643, -0.012095891670189781,
                  -0.008868858490542428, 1.5752662157441293
              ],
              "id": 303,
              "intrinsics": [0.04095, 0.04095, 0]
          }
      }],
      "robot-name": "9932CC",
      "timestamp": 1636114561.2718313,
      "version": 20190118
  }

  # (singulation_calibration, singulation_actionset, "SingulateLeftBin",
  # ({
  # "label":"SingulateLeftBin","depthTS":1652744143842,"pose2D":
  # {"x":272,"y":378},
  # "position3D":{"x":-0.409671783447266,"y":-0.776900172233582,
  # "z":-0.189233720302582},
  # "quaternion3D":{"w":-0.0102639803662896,"x":-0.000392893329262733,
  # "y":0.999215483665466,"z":-0.0382483936846256},
  # "tags":["full-autonomy"],
  # "userTS":1652744143842},),
  # {"commands":[{"movejPath":{"waypoints":[{"rotation":[0.870829343795776,
  # -0.564270853996277,1.19673097133636,-2.32055234909058,4.77512073516846,
  # -0.775123476982117],"blendRadius":0.05000000074505806,"velocity":2,
  # "acceleration":8}]}},{"setOutput":{"type":"vacuum","args":[{"intValue":1}]}
  # },{"movelPath":{"waypoints":[{"rotation":[0.87249493598938,
  # -0.370880752801895,1.12100052833557,-2.43831586837769,4.77492570877075,
  # -0.773466289043427],"velocity":1,"acceleration":4}]}},{"sleep":{"seconds":
  # 0.10000000149011612}},{"movelPath":{"waypoints":[{"rotation":[
  # 0.870768904685974,-0.57064825296402,1.19798243045807,-2.31542277336121,
  # 4.77512741088867,-0.775183618068695],"velocity":1,"acceleration":4}]}},
  # {"movejPath":{"waypoints":[{"rotation":[1.32486689090729,-1.03062188625336,
  # 1.807488322258,-2.35028171539307,4.73878049850464,-0.282691925764084],
  # "blendRadius":0.019999999552965164,"velocity":2,"acceleration":8},
  # {"rotation":[1.68677186965942,-0.785402238368988,1.60951948165894,
  # -2.45647430419922,4.68607711791992,0.0904752761125565],
  # "blendRadius":0.009999999776482582,"velocity":2,"acceleration":8}]}},
  # {"setOutput":{"type":"vacoff-blowon","args":[{"intValue":1}]}},{"sleep":
  # {"seconds":0.10000000149011612}},{"movejPath":{"waypoints":[{"rotation":
  # [1.22729384899139,-1.25325393676758,2.14721465110779,-2.53750061988831,
  # 4.69963312149048,-0.36921888589859],"velocity":2,"acceleration":8}]}},
  # {"setOutput":{"type":"blowoff","args":[{}]}}],"calibrationRequirement":{}},
  # ),

  return (
      (
          singulation_calibration,
          singulation_actionset,
          "SingulateLeftBin",
          ({
              "label": "SingulateLeftBin",
              "depthTS": 1652744143842,
              "pose2D": {
                  "x": 272,
                  "y": 378
              },
              "position3D": {
                  "x": -0.409671783447266,
                  "y": -0.776900172233582,
                  "z": -0.189233720302582
              },
              "quaternion3D": {
                  "w": -0.0102639803662896,
                  "x": -0.000392893329262733,
                  "y": 0.999215483665466,
                  "z": -0.0382483936846256
              },
              "tags": ["full-autonomy"],
              "userTS": 1652744143842
          },),
          {
              "commands": [{
                  "movejPath": {
                      "waypoints": [{
                          "rotation": [
                              0.870829343795776, -0.564270853996277,
                              1.19673097133636, -2.32055234909058,
                              4.77512073516846, -0.775123476982117
                          ],
                          "blendRadius": 0.05000000074505806,
                          "velocity": 2,
                          "acceleration": 8
                      }]
                  }
              }, {
                  "setOutput": {
                      "type": "vacuum",
                      "args": [{
                          "intValue": 1
                      }]
                  }
              }, {
                  "movelPath": {
                      "waypoints": [{
                          "rotation": [
                              0.87249493598938, -0.370880752801895,
                              1.12100052833557, -2.43831586837769,
                              4.77492570877075, -0.773466289043427
                          ],
                          "velocity": 1,
                          "acceleration": 4
                      }]
                  }
              }, {
                  "sleep": {
                      "seconds": 0.10000000149011612
                  }
              }, {
                  "movelPath": {
                      "waypoints": [{
                          "rotation": [
                              0.870768904685974, -0.57064825296402,
                              1.19798243045807, -2.31542277336121,
                              4.77512741088867, -0.775183618068695
                          ],
                          "velocity": 1,
                          "acceleration": 4
                      }]
                  }
              }, {
                  "movejPath": {
                      "waypoints": [{
                          "rotation": [
                              1.32486689090729, -1.03062188625336,
                              1.807488322258, -2.35028171539307,
                              4.73878049850464, -0.282691925764084
                          ],
                          "blendRadius": 0.019999999552965164,
                          "velocity": 2,
                          "acceleration": 8
                      }, {
                          "rotation": [
                              1.68677186965942, -0.785402238368988,
                              1.60951948165894, -2.45647430419922,
                              4.68607711791992, 0.0904752761125565
                          ],
                          "blendRadius": 0.009999999776482582,
                          "velocity": 2,
                          "acceleration": 8
                      }]
                  }
              }, {
                  "setOutput": {
                      "type": "vacoff-blowon",
                      "args": [{
                          "intValue": 1
                      }]
                  }
              }, {
                  "sleep": {
                      "seconds": 0.10000000149011612
                  }
              }, {
                  "movejPath": {
                      "waypoints": [{
                          "rotation": [
                              1.22729384899139, -1.25325393676758,
                              2.14721465110779, -2.53750061988831,
                              4.69963312149048, -0.36921888589859
                          ],
                          "velocity": 2,
                          "acceleration": 8
                      }]
                  }
              }, {
                  "setOutput": {
                      "type": "blowoff",
                      "args": [{}]
                  }
              }],
              "calibrationRequirement": {}
          },
      ),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 325,
              "y": 339
          },
          "position3D": {
              "x": -0.382841259241104,
              "y": -0.523214757442474,
              "z": -0.173133954405785
          },
          "quaternion3D": {
              "x": -9.06125860637985E-05,
              "y": 0.999908030033112,
              "z": -0.0103594865649939,
              "w": -0.00875430088490248
          },
          "tags": ["manual"],
          "userTS": 1651106653698
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1027,
              "y": 485
          },
          "position3D": {
              "x": 0.388690859079361,
              "y": -0.710125863552094,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": 4.2069427053093E-08,
              "y": 1,
              "z": -1.77635662764201E-15,
              "w": 6.46483044874913E-08
          },
          "tags": ["manual"],
          "userTS": 1651106656699
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.753571629524231, -1.04012715816498,
                          1.71001636981964, -2.26521563529968,
                          -1.59624767303467, -0.857579529285431
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.746945083141327, -0.963489472866058,
                          1.73761522769928, -2.36962056159973,
                          -1.59608423709869, -0.864206194877625
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.768907606601715, -1.17747735977173,
                          1.59329557418823, -2.01075172424316,
                          -1.59661984443665, -0.842243075370789
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.91427063941956, -0.711058616638184,
                          0.853917121887207, -1.68647849559784,
                          -1.57997250556946, 0.303356647491455
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.91439723968506, -0.711554765701294,
                          0.847501635551453, -1.6795654296875,
                          -1.57996904850006, 0.30348327755928
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.91463685035706, -0.712328970432281,
                          0.835092604160309, -1.666379570961, -1.57996273040771,
                          0.30372279882431
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 361,
              "y": 516
          },
          "position3D": {
              "x": -0.313139021396637,
              "y": -0.737186849117279,
              "z": -0.204200178384781
          },
          "quaternion3D": {
              "x": -0.00077449536183849,
              "y": 0.997277677059174,
              "z": 0.0105864033102989,
              "w": 0.0729699730873108
          },
          "tags": ["manual"],
          "userTS": 1651106690713
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1032,
              "y": 516
          },
          "position3D": {
              "x": 0.387746274471283,
              "y": -0.739023804664612,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106695715
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.958490252494812, -0.562005579471588,
                          0.884368658065796, -1.78337216377258,
                          -1.49125695228577, -0.660308182239532
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.959670662879944, -0.52583646774292,
                          0.943674445152283, -1.87894105911255,
                          -1.49112749099731, -0.659131109714508
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.955829620361328, -0.590561628341675,
                          0.651049137115479, -1.52128684520721,
                          -1.49154794216156, -0.66296112537384
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.90661942958832, -0.642042219638824,
                          0.728329420089722, -1.63829970359802,
                          -1.59247481822968, -0.227814540266991
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90686118602753, -0.642268896102905,
                          0.721475601196289, -1.63121378421783,
                          -1.59247052669525, -0.227572739124298
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90731823444366, -0.642502546310425,
                          0.708166062831879, -1.61766040325165,
                          -1.59246218204498, -0.227115735411644
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 322,
              "y": 462
          },
          "position3D": {
              "x": -0.36124512553215,
              "y": -0.677318394184113,
              "z": -0.182987481355667
          },
          "quaternion3D": {
              "x": -0.252400517463684,
              "y": 0.962219953536987,
              "z": 0.0885230898857117,
              "w": -0.0508965142071247
          },
          "tags": ["manual"],
          "userTS": 1651106704768
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1064,
              "y": 527
          },
          "position3D": {
              "x": 0.415553867816925,
              "y": -0.748418867588043,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106709770
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.04334807395935, -0.687480807304382,
                          1.11064505577087, -1.94358479976654,
                          -1.79656565189362, -1.07619988918304
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.02605485916138, -0.641413390636444,
                          1.15435492992401, -2.03733730316162,
                          -1.79740178585052, -1.09392404556274
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.08272135257721, -0.75177663564682,
                          0.940874755382538, -1.70053243637085,
                          -1.7944051027298, -1.03587210178375
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.93383347988129, -0.556250870227814,
                          0.565493762493134, -1.56067252159119,
                          -1.59195578098297, -0.20059922337532
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.93406438827515, -0.55554062128067,
                          0.556876361370087, -1.55276036262512,
                          -1.59195137023926, -0.200368195772171
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.93450117111206, -0.553888916969299,
                          0.539991736412048, -1.537517786026, -1.59194326400757,
                          -0.199931547045708
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 283,
              "y": 518
          },
          "position3D": {
              "x": -0.410904198884964,
              "y": -0.741281986236572,
              "z": -0.213061407208443
          },
          "quaternion3D": {
              "x": -0.263816118240356,
              "y": 0.957244098186493,
              "z": -0.0555348247289658,
              "w": -0.104884512722492
          },
          "tags": ["manual"],
          "userTS": 1651106793752
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1033,
              "y": 535
          },
          "position3D": {
              "x": 0.385190457105637,
              "y": -0.756209194660187,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106797804
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.947300016880035, -0.727395951747894,
                          1.37352788448334, -2.45819115638733,
                          -1.64333236217499, -1.2072948217392
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.938952147960663, -0.636160969734192,
                          1.33535814285278, -2.51183724403381,
                          -1.64133501052856, -1.21542108058929
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.967616140842438, -0.917651474475861,
                          1.40657579898834, -2.29950165748596,
                          -1.64817094802856, -1.18750810623169
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.89706897735596, -0.589114546775818,
                          0.628513336181641, -1.59161925315857,
                          -1.59265327453613, -0.237365499138832
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.89730834960938, -0.588841140270233,
                          0.620735704898834, -1.58410954475403,
                          -1.59264898300171, -0.237126186490059
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.89776062965393, -0.588073551654816,
                          0.605560958385468, -1.56969225406647,
                          -1.59264087677002, -0.236673891544342
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 388,
              "y": 352
          },
          "position3D": {
              "x": -0.314640283584595,
              "y": -0.527239263057709,
              "z": -0.2073635160923
          },
          "quaternion3D": {
              "x": -0.258708506822586,
              "y": 0.965753376483917,
              "z": 0.00812836829572916,
              "w": -0.0180095881223679
          },
          "tags": ["manual"],
          "userTS": 1651106802756
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1011,
              "y": 524
          },
          "position3D": {
              "x": 0.36694347858429,
              "y": -0.746522128582001,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106804806
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.861069083213806, -1.04623055458069, 1.8428475856781,
                          -2.3973560333252, -1.63165509700775, -1.27423417568207
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.851676225662231, -0.955495059490204,
                          1.85733914375305, -2.50315403938293,
                          -1.63137078285217, -1.2836400270462
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.882963299751282, -1.21792650222778, 1.7550003528595,
                          -2.13647222518921, -1.63229489326477,
                          -1.25230836868286
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.87996363639832, -0.652658045291901,
                          0.748313963413239, -1.64825296401978,
                          -1.59296774864197, -0.25447216629982
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.88021063804626, -0.652988910675049,
                          0.741647064685822, -1.64124941825867,
                          -1.59296345710754, -0.254225075244904
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.88067770004272, -0.653428196907043,
                          0.728708982467651, -1.62786149978638,
                          -1.59295523166656, -0.253758072853088
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 368,
              "y": 448
          },
          "position3D": {
              "x": -0.320147454738617,
              "y": -0.65429961681366,
              "z": -0.20997916162014
          },
          "quaternion3D": {
              "x": -0.2585409283638,
              "y": 0.965735852718353,
              "z": -0.0218703243881464,
              "w": 0.00570855895057321
          },
          "tags": ["manual"],
          "userTS": 1651106808759
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1040,
              "y": 520
          },
          "position3D": {
              "x": 0.39383265376091,
              "y": -0.742235064506531,
              "z": -0.0418440699577332
          },
          "quaternion3D": {
              "x": 0.258819073438644,
              "y": 0.965925872325897,
              "z": -5.3460194493482E-08,
              "w": 4.22219699203197E-08
          },
          "tags": ["manual"],
          "userTS": 1651106813813
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.923551976680756, -0.843783736228943,
                          1.47450125217438, -2.22701215744019,
                          -1.55693411827087, -1.21006464958191
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.920687735080719, -0.768973708152771,
                          1.48546075820923, -2.31274199485779,
                          -1.55686068534851, -1.21292817592621
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.930217325687408, -0.984605669975281,
                          1.39516842365265, -2.00694918632507,
                          -1.55710327625275, -1.20340096950531
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.89986300468445, -0.600072145462036,
                          0.646864354610443, -1.58938658237457,
                          -1.56556272506714, 0.812349259853363
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.89984107017517, -0.59960663318634,
                          0.638723492622375, -1.58171093463898,
                          -1.5655632019043, 0.812327206134796
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.8997997045517, -0.598471283912659,
                          0.622855961322784, -1.56697809696198,
                          -1.5655642747879, 0.812285840511322
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 414,
              "y": 371
          },
          "position3D": {
              "x": -0.265519797801971,
              "y": -0.562991380691528,
              "z": -0.178869590163231
          },
          "quaternion3D": {
              "x": -0.000198982859728858,
              "y": 0.999525964260101,
              "z": 0.00661368295550346,
              "w": 0.0300698988139629
          },
          "tags": ["manual"],
          "userTS": 1651106819818
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1041,
              "y": 526
          },
          "position3D": {
              "x": 0.393761843442917,
              "y": -0.747830033302307,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": 4.2069427053093E-08,
              "y": 1,
              "z": -1.77635662764201E-15,
              "w": 6.46483044874913E-08
          },
          "tags": ["manual"],
          "userTS": 1651106821816
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.909607946872711, -1.02980542182922,
                          1.68574678897858, -2.17253494262695,
                          -1.55933916568756, -0.702934265136719
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.905880212783813, -0.96128123998642,
                          1.72624957561493, -2.28152012825012,
                          -1.55954086780548, -0.706656813621521
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.91805374622345, -1.14496314525604, 1.53958404064178,
                          -1.91131353378296, -1.55888104438782,
                          -0.694500386714935
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.90491247177124, -0.58539754152298, 0.61926656961441,
                          -1.57757604122162, -1.5802264213562, 0.294001579284668
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90503621101379, -0.584776997566223,
                          0.610829591751099, -1.5697580575943,
                          -1.58022308349609, 0.294125229120255
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90527021884918, -0.58332622051239,
                          0.594355463981628, -1.55473220348358,
                          -1.58021688461304, 0.294359266757965
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 300,
              "y": 450
          },
          "position3D": {
              "x": -0.390606850385666,
              "y": -0.66391783952713,
              "z": -0.182806849479675
          },
          "quaternion3D": {
              "x": 1.14448394015199E-05,
              "y": 0.999859154224396,
              "z": 0.0167719200253487,
              "w": -0.000680461467709392
          },
          "tags": ["manual"],
          "userTS": 1651106834768
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1055,
              "y": 541
          },
          "position3D": {
              "x": 0.404479116201401,
              "y": -0.760842263698578,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": 4.2069427053093E-08,
              "y": 1,
              "z": -1.77635662764201E-15,
              "w": 6.46483044874913E-08
          },
          "tags": ["manual"],
          "userTS": 1651106836769
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.898546993732452, -0.725343227386475,
                          1.15484750270844, -1.9683586359024, -1.62067914009094,
                          -0.711955368518829
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.891689658164978, -0.675434768199921,
                          1.19639313220978, -2.06015586853027,
                          -1.62089669704437, -0.718817710876465
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.914191961288452, -0.799923121929169,
                          0.99338299036026, -1.73153805732727,
                          -1.62017250061035, -0.696299433708191
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.91170573234558, -0.50956779718399,
                          0.473226100206375, -1.50730192661285,
                          -1.58004212379456, 0.300792634487152
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.91182541847229, -0.507723212242126,
                          0.46237525343895, -1.49829423427582,
                          -1.58003890514374, 0.300912201404572
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.91205155849457, -0.503736913204193,
                          0.440873831510544, -1.48077654838562,
                          -1.58003294467926, 0.301138371229172
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 449,
              "y": 397
          },
          "position3D": {
              "x": -0.218617185950279,
              "y": -0.594166696071625,
              "z": -0.182003170251846
          },
          "quaternion3D": {
              "x": -0.000681890174746513,
              "y": 0.999096751213074,
              "z": 0.0386596173048019,
              "w": 0.0176241938024759
          },
          "tags": ["manual"],
          "userTS": 1651106838769
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1041,
              "y": 535
          },
          "position3D": {
              "x": 0.392679512500763,
              "y": -0.756180763244629,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": 4.2069427053093E-08,
              "y": 1,
              "z": -1.77635662764201E-15,
              "w": 6.46483044874913E-08
          },
          "tags": ["manual"],
          "userTS": 1651106842771
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.03727054595947, -0.962502181529999,
                          1.57187235355377, -2.08534336090088,
                          -1.60659050941467, -0.574520945549011
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.03035819530487, -0.904501080513, 1.62150239944458,
                          -2.19322371482849, -1.6072438955307,
                          -0.581407010555267
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.0527526140213, -1.05300962924957, 1.403315782547,
                          -1.8257395029068, -1.60511958599091,
                          -0.559099555015564
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.90050446987152, -0.556056141853333,
                          0.56316077709198, -1.55085337162018,
                          -1.58034563064575, 0.289594978094101
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90062844753265, -0.555041790008545,
                          0.553959906101227, -1.54266548156738,
                          -1.58034241199493, 0.289718866348267
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90086269378662, -0.552788019180298,
                          0.535918712615967, -1.52687549591064,
                          -1.58033609390259, 0.289953112602234
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 327,
              "y": 353
          },
          "position3D": {
              "x": -0.377108693122864,
              "y": -0.541724145412445,
              "z": -0.175860837101936
          },
          "quaternion3D": {
              "x": -4.2271403799532E-05,
              "y": 0.999942779541016,
              "z": 0.00979084428399801,
              "w": 0.00431941263377666
          },
          "tags": ["manual"],
          "userTS": 1651106846832
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1044,
              "y": 537
          },
          "position3D": {
              "x": 0.394502252340317,
              "y": -0.757865130901337,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": 4.2069427053093E-08,
              "y": 1,
              "z": -1.77635662764201E-15,
              "w": 6.46483044874913E-08
          },
          "tags": ["manual"],
          "userTS": 1651106850774
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.788279592990875, -0.976806461811066,
                          1.5943728685379, -2.16497421264648, -1.60695791244507,
                          -0.822692513465881
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.78119170665741, -0.910208344459534,
                          1.63042032718658, -2.26787710189819,
                          -1.60712242126465, -0.829782962799072
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.804479718208313, -1.09049940109253,
                          1.45770037174225, -1.91402626037598,
                          -1.60657334327698, -0.806486546993256
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.90188336372375, -0.545441329479218,
                          0.542735934257507, -1.54103028774261,
                          -1.58030843734741, 0.290973365306854
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90200650691986, -0.544262886047363,
                          0.533212542533875, -1.53268384933472,
                          -1.5803050994873, 0.291096568107605
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90223944187164, -0.541671097278595,
                          0.514503300189972, -1.51656377315521,
                          -1.58029890060425, 0.291329473257065
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 374,
              "y": 558
          },
          "position3D": {
              "x": -0.299683600664139,
              "y": -0.783905982971191,
              "z": -0.228494942188263
          },
          "quaternion3D": {
              "x": 5.7085864682449E-05,
              "y": 0.999937891960144,
              "z": 0.00613101804628968,
              "w": -0.00930899847298861
          },
          "tags": ["manual"],
          "userTS": 1651106863779
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1042,
              "y": 522
          },
          "position3D": {
              "x": 0.395969331264496,
              "y": -0.744479954242706,
              "z": -0.0418440699577332
          },
          "quaternion3D": {
              "x": 0.707106709480286,
              "y": 0.707106828689575,
              "z": 5.33850759154575E-08,
              "w": 3.09086267691328E-08
          },
          "tags": ["manual"],
          "userTS": 1651106868831
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.07665181159973, -0.51736181974411,
                          0.879573822021484, -1.91965758800507,
                          -1.61933493614197, -0.533848583698273
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.07049810886383, -0.466733574867249,
                          0.909782946109772, -2.00079441070557,
                          -1.61941587924957, -0.540008962154388
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.09072589874268, -0.590484797954559,
                          0.72991943359375, -1.69619858264923,
                          -1.61914134025574, -0.519759356975555
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.88771116733551, -0.615254282951355,
                          0.680257081985474, -1.62590098381042,
                          -1.54387402534485, 1.84733557701111
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.8874499797821, -0.615635335445404,
                          0.673708856105804, -1.61896467208862,
                          -1.54387640953064, 1.84707415103912
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.8869560956955, -0.616156697273254,
                          0.660962700843811, -1.60568380355835,
                          -1.54388093948364, 1.84658002853394
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 312,
              "y": 422
          },
          "position3D": {
              "x": -0.384606391191483,
              "y": -0.628717720508575,
              "z": -0.185554131865501
          },
          "quaternion3D": {
              "x": -0.258715629577637,
              "y": 0.965503692626953,
              "z": -0.0283900648355484,
              "w": -0.00793514493852854
          },
          "tags": ["manual"],
          "userTS": 1651106871838
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1028,
              "y": 524
          },
          "position3D": {
              "x": 0.38231697678566,
              "y": -0.746132850646973,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106874834
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.83229386806488, -0.880737125873566, 1.4780775308609,
                          -2.2222797870636, -1.55843687057495, -1.30123853683472
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.829476535320282, -0.805926263332367,
                          1.48927664756775, -2.3082549571991, -1.55828404426575,
                          -1.3040519952774
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.838901460170746, -1.02148258686066,
                          1.39821934700012, -2.00175642967224,
                          -1.55879366397858, -1.29464018344879
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.89767742156982, -0.628606379032135,
                          0.703180730342865, -1.62678146362305,
                          -1.59264194965363, -0.236757069826126
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.8979195356369, -0.628724098205566,
                          0.696130573749542, -1.61960816383362,
                          -1.5926376581192, -0.236514925956726
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.89837729930878, -0.628739774227142,
                          0.682424366474152, -1.60587584972382,
                          -1.59262943267822, -0.23605714738369
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 379,
              "y": 370
          },
          "position3D": {
              "x": -0.318767100572586,
              "y": -0.55485475063324,
              "z": -0.19858281314373
          },
          "quaternion3D": {
              "x": -0.25882625579834,
              "y": 0.965780019760132,
              "z": -0.00163537124171853,
              "w": 0.0165914017707109
          },
          "tags": ["manual"],
          "userTS": 1651106878785
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1045,
              "y": 530
          },
          "position3D": {
              "x": 0.397531002759933,
              "y": -0.750941455364227,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106881786
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.844253182411194, -0.995198547840118,
                          1.70113563537598, -2.2606189250946, -1.57677149772644,
                          -1.29067254066467
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.839701473712921, -0.916451454162598,
                          1.72413289546967, -2.36239075660706,
                          -1.57684445381165, -1.29522371292114
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.854751944541931, -1.13910591602325,
                          1.59488022327423, -2.01039409637451,
                          -1.57660102844238, -1.28017508983612
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.91289842128754, -0.58431750535965,
                          0.619294464588165, -1.58685386180878,
                          -1.59235656261444, -0.221535176038742
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.91313469409943, -0.583977282047272,
                          0.611389994621277, -1.57928419113159,
                          -1.59235215187073, -0.22129887342453
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.91358149051666, -0.583076238632202,
                          0.595960199832916, -1.56474554538727,
                          -1.59234404563904, -0.220852077007294
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 312,
              "y": 473
          },
          "position3D": {
              "x": -0.381054580211639,
              "y": -0.687287509441376,
              "z": -0.203929483890533
          },
          "quaternion3D": {
              "x": -0.258713603019714,
              "y": 0.965236306190491,
              "z": 0.00763250980526209,
              "w": -0.036441046744585
          },
          "tags": ["manual"],
          "userTS": 1651106889848
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1038,
              "y": 535
          },
          "position3D": {
              "x": 0.389966249465942,
              "y": -0.755812406539917,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106891840
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.945798695087433, -0.739767074584961,
                          1.27325212955475, -2.15826916694641,
                          -1.65647220611572, -1.19085812568665
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.936756491661072, -0.670970380306244,
                          1.28206920623779, -2.23665618896484,
                          -1.65598034858704, -1.19992005825043
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.96690958738327, -0.866985201835632,
                          1.19599282741547, -1.95196914672852,
                          -1.65759110450745, -1.16969871520996
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.90256297588348, -0.581423580646515,
                          0.613836765289307, -1.5845137834549,
                          -1.59255087375641, -0.23187118768692
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90280079841614, -0.581058204174042,
                          0.60588413476944, -1.57692122459412,
                          -1.59254658222198, -0.231633305549622
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90325045585632, -0.580105721950531,
                          0.590355455875397, -1.56233489513397,
                          -1.5925384759903, -0.231183722615242
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 273,
              "y": 530
          },
          "position3D": {
              "x": -0.417057305574417,
              "y": -0.754931271076202,
              "z": -0.207977622747421
          },
          "quaternion3D": {
              "x": -0.258420675992966,
              "y": 0.965566277503967,
              "z": 0.0172901675105095,
              "w": -0.0245275869965553
          },
          "tags": ["manual"],
          "userTS": 1651106893843
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1038,
              "y": 527
          },
          "position3D": {
              "x": 0.390716433525085,
              "y": -0.748658180236816,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106896847
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.958103775978088, -0.512492895126343,
                          0.827461004257202, -1.90791237354279,
                          -1.65669906139374, -1.17687940597534
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.949998021125793, -0.457069784402847,
                          0.845620393753052, -1.98219227790833,
                          -1.65651631355286, -1.18501329421997
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.976890742778778, -0.598194420337677,
                          0.705506205558777, -1.69863486289978,
                          -1.65709888935089, -1.15802693367004
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.90617859363556, -0.605272889137268,
                          0.659123241901398, -1.60587251186371,
                          -1.59248316287994, -0.228255391120911
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90641748905182, -0.605163097381592,
                          0.651653289794922, -1.59850692749023,
                          -1.59247887134552, -0.228016421198845
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90686929225922, -0.604725241661072,
                          0.63710343837738, -1.5843847990036, -1.59247064590454,
                          -0.227564677596092
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 325,
              "y": 347
          },
          "position3D": {
              "x": -0.375591695308685,
              "y": -0.537325859069824,
              "z": -0.164577588438988
          },
          "quaternion3D": {
              "x": -0.258308202028275,
              "y": 0.964504778385162,
              "z": 0.0163930710405111,
              "w": -0.0523322708904743
          },
          "tags": ["manual"],
          "userTS": 1651106899849
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1044,
              "y": 500
          },
          "position3D": {
              "x": 0.401543170213699,
              "y": -0.723792612552643,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106901845
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.835551738739014, -1.06183123588562,
                          1.75123655796051, -2.34066534042358,
                          -1.68196678161621, -1.30279350280762
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.8226717710495, -0.978715300559998, 1.76868557929993,
                          -2.44265675544739, -1.6809219121933, -1.31570994853973
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.865925252437592, -1.21672165393829,
                          1.65738379955292, -2.08850502967834,
                          -1.68435549736023, -1.27232205867767
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.92855501174927, -0.665069699287415,
                          0.771149277687073, -1.65762114524841,
                          -1.59205770492554, -0.205877840518951
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.92879498004913, -0.665463626384735,
                          0.764589726924896, -1.65066242218018,
                          -1.59205317497253, -0.205637872219086
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.92924857139587, -0.666028797626495,
                          0.751869559288025, -1.63736701011658,
                          -1.59204471111298, -0.205184280872345
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 400,
              "y": 463
          },
          "position3D": {
              "x": -0.279036372900009,
              "y": -0.672660827636719,
              "z": -0.212741076946259
          },
          "quaternion3D": {
              "x": -0.258253067731857,
              "y": 0.965143978595734,
              "z": 0.0187602508813143,
              "w": -0.0380869023501873
          },
          "tags": ["manual"],
          "userTS": 1651106908847
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1041,
              "y": 523
          },
          "position3D": {
              "x": 0.394671410322189,
              "y": -0.745310008525848,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106910847
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.06510591506958, -0.821709096431732,
                          1.45197367668152, -2.23066806793213, -1.680140376091,
                          -1.07024168968201
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.05371141433716, -0.749930024147034,
                          1.46574878692627, -2.31747078895569,
                          -1.67979550361633, -1.08169889450073
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.09152376651764, -0.954797148704529,
                          1.36576676368713, -2.00846409797668, -1.6808830499649,
                          -1.04367423057556
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.91194033622742, -0.609373807907104,
                          0.66684901714325, -1.6093727350235, -1.59237456321716,
                          -0.222493335604668
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.91217851638794, -0.60930073261261,
                          0.659447371959686, -1.60203874111176,
                          -1.59237027168274, -0.222255066037178
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.91262900829315, -0.608936607837677,
                          0.645035982131958, -1.58798146247864,
                          -1.59236204624176, -0.221804618835449
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 379,
              "y": 370
          },
          "position3D": {
              "x": -0.312321990728378,
              "y": -0.559117794036865,
              "z": -0.185636326670647
          },
          "quaternion3D": {
              "x": -0.258844673633575,
              "y": 0.965870440006256,
              "z": -0.00219942117109895,
              "w": -0.00942674279212952
          },
          "tags": ["manual"],
          "userTS": 1651106912797
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1033,
              "y": 513
          },
          "position3D": {
              "x": 0.388617813587189,
              "y": -0.736047506332397,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106915850
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.877723276615143, -1.03772461414337,
                          1.74852967262268, -2.30842804908752,
                          -1.60536777973175, -1.25724422931671
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.870749831199646, -0.955276787281036,
                          1.76878786087036, -2.41137433052063,
                          -1.60517942905426, -1.26421928405762
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.893967747688293, -1.19018971920013,
                          1.64838802814484, -2.05525588989258,
                          -1.60579788684845, -1.24099576473236
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.90879642963409, -0.649828553199768,
                          0.742871940135956, -1.64500880241394,
                          -1.59243392944336, -0.22563736140728
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90903842449188, -0.650117337703705,
                          0.736128866672516, -1.6379714012146,
                          -1.59242951869965, -0.225395306944847
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90949606895447, -0.650474011898041,
                          0.723040521144867, -1.624516248703, -1.59242117404938,
                          -0.224937796592712
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 329,
              "y": 369
          },
          "position3D": {
              "x": -0.367236405611038,
              "y": -0.564696907997131,
              "z": -0.169956788420677
          },
          "quaternion3D": {
              "x": -0.258799374103546,
              "y": 0.965812146663666,
              "z": 0.00325277890078723,
              "w": -0.0148064522072673
          },
          "tags": ["manual"],
          "userTS": 1651106917850
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1027,
              "y": 517
          },
          "position3D": {
              "x": 0.382770925760269,
              "y": -0.739385783672333,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106919857
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.828836500644684, -0.999438583850861,
                          1.63399410247803, -2.23706698417664,
                          -1.61899065971375, -1.30640733242035
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.821303427219391, -0.924276649951935,
                          1.65694999694824, -2.33554720878601,
                          -1.61874997615814, -1.31394529342651
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          0.846404016017914, -1.13617610931396,
                          1.52775478363037, -1.9932382106781, -1.61953914165497,
                          -1.28882813453674
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.90081071853638, -0.649245619773865,
                          0.741827964782715, -1.64472115039825,
                          -1.59258365631104, -0.233623564243317
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90105402469635, -0.649535238742828,
                          0.735086739063263, -1.63768482208252,
                          -1.59257924556732, -0.233380258083344
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90151405334473, -0.649893045425415,
                          0.722001075744629, -1.62423098087311,
                          -1.59257090091705, -0.232920244336128
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 435,
              "y": 399
          },
          "position3D": {
              "x": -0.22863607108593,
              "y": -0.602128267288208,
              "z": -0.164738610386848
          },
          "quaternion3D": {
              "x": -0.258464515209198,
              "y": 0.965714514255524,
              "z": 0.0195073410868645,
              "w": -0.0145279308781028
          },
          "tags": ["manual"],
          "userTS": 1651106925803
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1029,
              "y": 516
          },
          "position3D": {
              "x": 0.384507566690445,
              "y": -0.738443195819855,
              "z": -0.0418439209461212
          },
          "quaternion3D": {
              "x": -0.258819073438644,
              "y": 0.965925812721252,
              "z": 5.34601909407684E-08,
              "w": 4.22219628148923E-08
          },
          "tags": ["manual"],
          "userTS": 1651106929805
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.05691862106323, -1.03202795982361, 1.66365802288055,
                          -2.19876980781555, -1.64728367328644,
                          -1.07720363140106
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.04669547080994, -0.961581349372864,
                          1.69778037071228, -2.30412244796753,
                          -1.64731681346893, -1.08745670318604
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.08045566082001, -1.15395021438599, 1.53189098834991,
                          -1.94327795505524, -1.64717543125153,
                          -1.05359792709351
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.90316188335419, -0.64928674697876,
                          0.741891622543335, -1.64469254016876,
                          -1.59253966808319, -0.231272205710411
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90340483188629, -0.649575293064117,
                          0.735148429870605, -1.63765525817871,
                          -1.59253525733948, -0.23102930188179
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.90386414527893, -0.649930894374847,
                          0.722058653831482, -1.62419962882996,
                          -1.5925270318985, -0.230570018291473
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "FlipAction", ({
          "label": "FlipAction",
          "pose2D": {
              "x": 362,
              "y": 519
          },
          "position3D": {
              "x": -0.309039890766144,
              "y": -0.741633772850037,
              "z": -0.201218396425247
          },
          "quaternion3D": {
              "x": -0.259296864271164,
              "y": 0.964558064937592,
              "z": -0.0054976656101644,
              "w": -0.0486074723303318
          },
          "tags": ["manual"],
          "userTS": 1651106934854
      }, {
          "label": "FlipAction",
          "pose2D": {
              "x": 1042,
              "y": 531
          },
          "position3D": {
              "x": 0.394477993249893,
              "y": -0.751836538314819,
              "z": -0.0418438613414764
          },
          "quaternion3D": {
              "x": -0.499999940395355,
              "y": 0.866025447845459,
              "z": 6.40025419329504E-08,
              "w": 1.67817546525839E-08
          },
          "tags": ["manual"],
          "userTS": 1651106938808
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.36442387104034, -1.2956885099411, 1.87530171871185,
                          -2.22823095321655, -1.50674259662628,
                          -0.389890968799591
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.06321001052856, -0.724337995052338,
                          1.24625861644745, -2.17225909233093,
                          -1.66131258010864, -1.07570517063141
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.05381321907043, -0.654520690441132,
                          1.25114715099335, -2.24781155586243,
                          -1.66056156158447, -1.08510994911194
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.08523058891296, -0.854622602462769,
                          1.17773199081421, -1.97143614292145, -1.6630392074585,
                          -1.05366063117981
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78604388237, -1.18071150779724, 1.69951498508453,
                          -2.18677163124084, -1.54413878917694,
                          0.030530845746398
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }, {
                      "rotation": [
                          1.91053509712219, -0.611187100410461,
                          0.673690855503082, -1.62776350975037,
                          -1.59894025325775, -0.747623205184937
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.91082525253296, -0.611595809459686,
                          0.66719651222229, -1.62085223197937,
                          -1.59893894195557, -0.74733293056488
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "sleep": {
                  "seconds": 0.10000000149011612
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.91137385368347, -0.612169802188873,
                          0.654552221298218, -1.60761845111847,
                          -1.5989363193512, -0.746783971786499
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.22566604614258, -1.77517175674438, 2.38923001289368,
                          -2.25241446495056, -1.5004073381424,
                          -0.498422652482986
                      ],
                      "velocity": 1.0,
                      "acceleration": 1.0
                  }]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "pose2D": {
              "x": 309,
              "y": 454
          },
          "position3D": {
              "x": -0.377366840839386,
              "y": -0.668716669082642,
              "z": -0.180435910820961
          },
          "quaternion3D": {
              "x": 4.2069427053093E-08,
              "y": 1,
              "z": -1.77635662764201E-15,
              "w": 6.46483044874913E-08
          }
      }, {
          "pose2D": {
              "x": 811,
              "y": 366
          },
          "position3D": {
              "x": 0.249415248632431,
              "y": -0.525295615196228,
              "z": -0.244113385677338
          },
          "quaternion3D": {
              "x": 4.2069427053093E-08,
              "y": 1,
              "z": -1.77635662764201E-15,
              "w": 6.46483044874913E-08
          }
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          0.901756167411804, -0.831171452999115,
                          1.03106558322906, -1.76407361030579,
                          -1.59871602058411, -0.709192037582397
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.897429466247559, -0.71590793132782,
                          1.25013101100922, -2.09852576255798, -1.5987389087677,
                          -0.713519275188446
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.901560962200165, -0.82861065864563, 1.0455367565155,
                          -1.78110861778259, -1.59871971607208,
                          -0.709386885166168
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78011989593506, -1.24063885211945, 1.71240437030792,
                          -2.01685380935669, -1.5835245847702, 0.169243082404137
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.79219484329224, -0.99922901391983, 1.88248205184937,
                          -2.42818999290466, -1.5832132101059, 0.181316435337067
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.77966773509979, -1.24680733680725, 1.70254075527191,
                          -2.00082731246948, -1.58353674411774,
                          0.168791964650154
                      ],
                      "velocity": 1.0,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", (
          {
              "label": "Kit",
              "pose2D": {
                  "x": 355,
                  "y": 519
              },
              "position3D": {
                  "x": -0.324990600347519,
                  "y": -0.740210056304932,
                  "z": -0.218312799930573
              },
              "quaternion3D": {
                  "x": 4.2069427053093E-08,
                  "y": 1,
                  "z": -1.77635662764201E-15,
                  "w": 6.46483044874913E-08
              },
              "tags": ["manual"],
              "userTS": 1651103568366
          },
          {
              "label": "Kit",
              "pose2D": {
                  "x": 736,
                  "y": 377
              },
              "position3D": {
                  "x": 0.147099822759628,
                  "y": -0.543265819549561,
                  "z": -0.241073206067085
              },
              "quaternion3D": {
                  "x": -0.309016942977905,
                  "y": 0.95105654001236,
                  "z": 1.35075595153467E-08,
                  "w": 2.04985770579924E-08
              },
              "tags": ["manual"],
              "userTS": 1651103577381
          },
      ), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.00795757770538, -0.690242111682892,
                          0.875154674053192, -1.746169090271, -1.59785723686218,
                          -0.602953791618347
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.00547575950623, -0.573808789253235,
                          1.07676529884338, -2.0642831325531, -1.59787571430206,
                          -0.605435490608215
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.0078456401825, -0.687723636627197,
                          0.889376997947693, -1.76291024684906,
                          -1.59786057472229, -0.603065192699432
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.62126350402832, -1.28746795654297, 1.77252852916718,
                          -2.04672646522522, -1.59799087047577,
                          -0.617971122264862
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.6174396276474, -1.04169034957886, 1.95809674263,
                          -2.47817659378052, -1.59802520275116,
                          -0.621794879436493
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.62141919136047, -1.29355442523956, 1.76210975646973,
                          -2.03021717071533, -1.59798991680145,
                          -0.617814779281616
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 387,
              "y": 355
          },
          "position3D": {
              "x": -0.315187692642212,
              "y": -0.531923115253448,
              "z": -0.207543686032295
          },
          "quaternion3D": {
              "x": -0.309016942977905,
              "y": 0.95105654001236,
              "z": 1.35075595153467E-08,
              "w": 2.04985770579924E-08
          },
          "tags": ["manual"],
          "userTS": 1651103581374
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 783,
              "y": 365
          },
          "position3D": {
              "x": 0.213221490383148,
              "y": -0.522448837757111,
              "z": -0.248115360736847
          },
          "quaternion3D": {
              "x": -0.309016942977905,
              "y": 0.95105654001236,
              "z": 1.35075595153467E-08,
              "w": 2.04985770579924E-08
          },
          "tags": ["manual"],
          "userTS": 1651103585375
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          0.8494992852211, -1.17934262752533, 1.67298686504364,
                          -2.07686996459961, -1.5966579914093, -1.39002013206482
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.832599699497223, -0.961095750331879,
                          1.82524812221527, -2.44781184196472,
                          -1.59643864631653, -1.40692341327667
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.848734259605408, -1.1719651222229, 1.68325281143188,
                          -2.09453296661377, -1.59665191173553,
                          -1.39078509807587
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.7413045167923, -1.27415025234222, 1.77398884296417,
                          -2.0583131313324, -1.59670174121857,
                          -0.497894674539566
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.74010169506073, -1.02371370792389, 1.95194756984711,
                          -2.48673987388611, -1.5967161655426, -0.49909633398056
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.74136078357697, -1.28046274185181, 1.76384294033051,
                          -2.04185342788696, -1.59670162200928,
                          -0.497837692499161
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 280,
              "y": 524
          },
          "position3D": {
              "x": -0.411963939666748,
              "y": -0.747989118099213,
              "z": -0.210666939616203
          },
          "quaternion3D": {
              "x": -0.309016942977905,
              "y": 0.95105654001236,
              "z": 1.35075595153467E-08,
              "w": 2.04985770579924E-08
          },
          "tags": ["manual"],
          "userTS": 1651103592378
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 838,
              "y": 375
          },
          "position3D": {
              "x": 0.281294673681259,
              "y": -0.540729999542236,
              "z": -0.231737121939659
          },
          "quaternion3D": {
              "x": -0.309016942977905,
              "y": 0.95105654001236,
              "z": 1.35075595153467E-08,
              "w": 2.04985770579924E-08
          },
          "tags": ["manual"],
          "userTS": 1651103592378
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          0.932739019393921, -0.575564086437225,
                          0.64482456445694, -1.65029263496399,
                          -1.59760189056396, -1.30675685405731
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.921434879302979, -0.484505861997604,
                          0.878701746463776, -1.97552931308746,
                          -1.59747862815857, -1.3180638551712
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.93222576379776, -0.575063586235046,
                          0.662464320659637, -1.66844606399536,
                          -1.59759998321533, -1.30726993083954
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.84668838977814, -1.19160783290863, 1.61095583438873,
                          -1.97516548633575, -1.59526193141937,
                          -0.39248713850975
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.84770023822784, -0.98034143447876, 1.80271780490875,
                          -2.37816953659058, -1.59524643421173,
                          -0.391473680734634
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.84665989875793, -1.19668650627136, 1.60025405883789,
                          -1.9593859910965, -1.59526288509369,
                          -0.392515033483505
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 452,
              "y": 398
          },
          "position3D": {
              "x": -0.214554965496063,
              "y": -0.595809519290924,
              "z": -0.182209849357605
          },
          "quaternion3D": {
              "x": -0.309016942977905,
              "y": 0.95105654001236,
              "z": 1.35075595153467E-08,
              "w": 2.04985770579924E-08
          },
          "tags": ["manual"],
          "userTS": 1651103601384
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 756,
              "y": 361
          },
          "position3D": {
              "x": 0.17595311999321,
              "y": -0.517335951328278,
              "z": -0.2481509745121
          },
          "quaternion3D": {
              "x": -0.309016942977905,
              "y": 0.95105654001236,
              "z": 1.35075595153467E-08,
              "w": 2.04985770579924E-08
          },
          "tags": ["manual"],
          "userTS": 1651103606383
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.04271817207336, -1.166020154953, 1.58003199100494,
                          -1.99203944206238, -1.59856331348419,
                          -1.19674098491669
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.02886927127838, -0.978188872337341, 1.760697722435,
                          -2.360919713974, -1.59845459461212, -1.21059417724609
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.04209268093109, -1.1600786447525, 1.59162044525146,
                          -2.00958585739136, -1.5985621213913, -1.19736635684967
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.67649722099304, -1.3138200044632, 1.82770311832428,
                          -2.07406139373779, -1.59744536876678,
                          -0.562720060348511
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.673792719841, -1.05197072029114, 2.00757694244385,
                          -2.51585674285889, -1.59747350215912,
                          -0.565423905849457
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.67661070823669, -1.32039964199066, 1.81748270988464,
                          -2.05725836753845, -1.59744465351105,
                          -0.562605857849121
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 442,
              "y": 527
          },
          "position3D": {
              "x": -0.222248330712318,
              "y": -0.746761977672577,
              "z": -0.231947422027588
          },
          "quaternion3D": {
              "x": -0.309016942977905,
              "y": 0.95105654001236,
              "z": 1.35075595153467E-08,
              "w": 2.04985770579924E-08
          },
          "tags": ["manual"],
          "userTS": 1651103609384
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 809,
              "y": 368
          },
          "position3D": {
              "x": 0.247429624199867,
              "y": -0.526268303394318,
              "z": -0.247908532619476
          },
          "quaternion3D": {
              "x": -0.309016942977905,
              "y": 0.95105654001236,
              "z": 1.35075595153467E-08,
              "w": 2.04985770579924E-08
          },
          "tags": ["manual"],
          "userTS": 1651103613386
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.13302540779114, -0.782545983791351,
                          1.08345973491669, -1.87640714645386,
                          -1.59910225868225, -1.10639977455139
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.12299072742462, -0.631389558315277, 1.2402241230011,
                          -2.18461179733276, -1.59904778003693,
                          -1.11643779277802
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.13257110118866, -0.777976453304291,
                          1.09465432167053, -1.89218282699585,
                          -1.59910333156586, -1.10685384273529
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.79808926582336, -1.23637437820435, 1.72077441215515,
                          -2.04142379760742, -1.59596073627472,
                          -0.441096246242523
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.79812479019165, -0.996462047100067,
                          1.89745771884918, -2.45801901817322,
                          -1.59595990180969, -0.441059201955795
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.79809832572937, -1.24242377281189, 1.71067070960999,
                          -2.02527070045471, -1.59596109390259,
                          -0.441086500883102
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 368,
              "y": 450
          },
          "position3D": {
              "x": -0.320890426635742,
              "y": -0.656979501247406,
              "z": -0.213036775588989
          },
          "quaternion3D": {
              "x": -0.309016942977905,
              "y": 0.95105654001236,
              "z": 1.35075595153467E-08,
              "w": 2.04985770579924E-08
          },
          "tags": ["manual"],
          "userTS": 1651103615387
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 760,
              "y": 366
          },
          "position3D": {
              "x": 0.18043464422226,
              "y": -0.526613235473633,
              "z": -0.243765339255333
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103624393
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          0.958975255489349, -0.922400712966919,
                          1.27900373935699, -1.93692827224731,
                          -1.59786117076874, -1.28051245212555
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.946013152599335, -0.756148636341095,
                          1.43621802330017, -2.26074385643005,
                          -1.59772956371307, -1.29347801208496
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.958387970924377, -0.917101562023163,
                          1.28982317447662, -1.95306217670441,
                          -1.59785890579224, -1.28109955787659
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.68954014778137, -1.30246376991272, 1.80190515518188,
                          -2.06650924682617, -1.59923911094666,
                          -0.811565518379211
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.68150901794434, -1.04844272136688, 1.98474311828613,
                          -2.50359702110291, -1.59926760196686,
                          -0.819598257541656
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.68985486030579, -1.30880391597748, 1.79158663749695,
                          -2.04984211921692, -1.59923827648163,
                          -0.811249673366547
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 361,
              "y": 355
          },
          "position3D": {
              "x": -0.354362636804581,
              "y": -0.528999865055084,
              "z": -0.218477115035057
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103638345
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 840,
              "y": 372
          },
          "position3D": {
              "x": 0.288965165615082,
              "y": -0.53185099363327,
              "z": -0.247393056750298
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103642346
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          0.798025250434875, -1.14000725746155,
                          1.64816200733185, -2.09874606132507,
                          -1.59156882762909, -1.70333898067474
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.778711378574371, -0.914888739585876,
                          1.77924883365631, -2.45534539222717,
                          -1.59117782115936, -1.72265207767487
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.797146081924438, -1.13213050365448,
                          1.65747439861298, -2.11595416069031,
                          -1.59155476093292, -1.70421779155731
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.87008905410767, -1.18914389610291, 1.6533282995224,
                          -2.02620410919189, -1.59810709953308,
                          -0.630949735641479
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.86628246307373, -0.962022304534912,
                          1.83013463020325, -2.43023657798767,
                          -1.59813988208771, -0.634756088256836
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.87024343013763, -1.19484376907349, 1.64320492744446,
                          -2.01037693023682, -1.59810626506805,
                          -0.630794405937195
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 326,
              "y": 373
          },
          "position3D": {
              "x": -0.380456238985062,
              "y": -0.564419865608215,
              "z": -0.187531307339668
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103648349
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 765,
              "y": 356
          },
          "position3D": {
              "x": 0.188256934285164,
              "y": -0.510594010353088,
              "z": -0.245944142341614
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103650402
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          0.807127416133881, -1.07640647888184,
                          1.46275341510773, -1.97674834728241,
                          -1.59174811840057, -1.6942366361618
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.789178550243378, -0.893040955066681,
                          1.62325859069824, -2.32098865509033,
                          -1.59138798713684, -1.71218490600586
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.806309998035431, -1.07042753696442,
                          1.47350943088531, -1.99350130558014,
                          -1.59173548221588, -1.69505369663239
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.70733714103699, -1.3265233039856, 1.83973407745361,
                          -2.07977294921875, -1.59916818141937,
                          -0.793761432170868
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.69949638843536, -1.06296372413635, 2.02185225486755,
                          -2.52567362785339, -1.59920001029968, -0.8016037940979
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.70764482021332, -1.33311569690704, 1.829434633255,
                          -2.06287264823914, -1.59916734695435,
                          -0.793452739715576
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 381,
              "y": 564
          },
          "position3D": {
              "x": -0.28867781162262,
              "y": -0.791536867618561,
              "z": -0.22806590795517
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103654356
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 861,
              "y": 403
          },
          "position3D": {
              "x": 0.30682510137558,
              "y": -0.579766035079956,
              "z": -0.229509964585304
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103661357
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.08466005325317, -0.617522537708282,
                          0.770068526268005, -1.73645651340485,
                          -1.59631764888763, -1.4166659116745
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.07217669487, -0.497119575738907, 0.954110622406006,
                          -2.04121732711792, -1.59614634513855, -1.4291512966156
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.08409261703491, -0.614936351776123,
                          0.783946752548218, -1.75293517112732,
                          -1.59631371498108, -1.41723310947418
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.8745402097702, -1.09494483470917, 1.46278321743011,
                          -1.92973673343658, -1.59806776046753,
                          -0.626497089862823
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.8711189031601, -0.907792210578918, 1.65902817249298,
                          -2.313227891922, -1.59809756278992, -0.629917979240417
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.8746794462204, -1.09927487373352, 1.45178139209747,
                          -1.9144012928009, -1.59806704521179,
                          -0.626356899738312
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 727,
              "y": 364
          },
          "position3D": {
              "x": 0.135227084159851,
              "y": -0.523125529289246,
              "z": -0.245185792446136
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103683418
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 308,
              "y": 368
          },
          "position3D": {
              "x": -0.407959282398224,
              "y": -0.555693507194519,
              "z": -0.194937214255333
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103685417
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.60589957237244, -1.27610468864441, 1.92164099216461,
                          -2.21499347686768, -1.59945797920227,
                          -0.895239889621735
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.59551250934601, -0.992706418037415,
                          2.05239200592041, -2.62944197654724, -1.5994645357132,
                          -0.90563029050827
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.60543346405029, -1.26613903045654, 1.93103420734406,
                          -2.23436379432678, -1.59946155548096,
                          -0.895705699920654
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          0.771982252597809, -1.08859860897064,
                          1.36790251731873, -1.87042462825775,
                          -1.59104144573212, -1.72938215732574
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.754568994045258, -0.919735133647919,
                          1.5755113363266, -2.2472460269928, -1.59068405628204,
                          -1.74679374694824
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.772655367851257, -1.09226953983307,
                          1.35636234283447, -1.85520052909851,
                          -1.59105503559113, -1.72870814800262
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 758,
              "y": 361
          },
          "position3D": {
              "x": 0.177993476390839,
              "y": -0.5187748670578,
              "z": -0.243631780147552
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103687415
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 330,
              "y": 478
          },
          "position3D": {
              "x": -0.3656145632267,
              "y": -0.691305041313171,
              "z": -0.218356385827065
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103688416
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.68530511856079, -1.25974404811859, 1.89302515983582,
                          -2.20046854019165, -1.5992614030838,
                          -0.815802097320557
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.67679691314697, -0.984532475471497, 2.0252583026886,
                          -2.60815739631653, -1.59928548336029,
                          -0.824312925338745
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.68492352962494, -1.25008189678192, 1.90245926380157,
                          -2.21957349777222, -1.59926557540894,
                          -0.816183388233185
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          0.939481735229492, -0.834290862083435,
                          1.01234865188599, -1.7655189037323, -1.59414637088776,
                          -1.5618714094162
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.925202667713165, -0.698597848415375,
                          1.22619903087616, -2.11539363861084,
                          -1.59390556812286, -1.57615089416504
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.94003438949585, -0.836593925952911,
                          0.999616742134094, -1.75047147274017,
                          -1.59415555000305, -1.56131792068481
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 805,
              "y": 364
          },
          "position3D": {
              "x": 0.24091599881649,
              "y": -0.523192822933197,
              "z": -0.238937452435493
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103689416
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 421,
              "y": 400
          },
          "position3D": {
              "x": -0.249414339661598,
              "y": -0.600658178329468,
              "z": -0.174217149615288
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103690413
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.79461765289307, -1.20753991603851, 1.8022997379303,
                          -2.15886259078979, -1.59869778156281,
                          -0.706447601318359
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78885126113892, -0.955186188220978,
                          1.93788874149323, -2.54696869850159,
                          -1.59873044490814, -0.712215185165405
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.79435896873474, -1.1987224817276, 1.81182944774628,
                          -2.17721462249756, -1.59870195388794,
                          -0.706705927848816
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.00298881530762, -1.18169605731964, 1.44895470142365,
                          -1.8532041311264, -1.59515690803528, -1.49835431575775
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.986277759075165, -1.01950299739838,
                          1.68413162231445, -2.25097894668579,
                          -1.59489977359772, -1.51506686210632
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.00363409519196, -1.18491172790527, 1.43646955490112,
                          -1.83748817443848, -1.59516668319702, -1.4977080821991
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 729,
              "y": 369
          },
          "position3D": {
              "x": 0.138471335172653,
              "y": -0.530602157115936,
              "z": -0.245369389653206
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103693417
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 303,
              "y": 500
          },
          "position3D": {
              "x": -0.385577946901321,
              "y": -0.720139861106873,
              "z": -0.20249916613102
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103693417
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.61137187480927, -1.25921702384949, 1.89846193790436,
                          -2.20854520797729, -1.59945023059845,
                          -0.889765322208405
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.60126233100891, -0.981445252895355,
                          2.02839016914368, -2.61653661727905,
                          -1.59945809841156, -0.899878144264221
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.61091816425323, -1.24943101406097, 1.907799243927,
                          -2.22767972946167, -1.59945380687714,
                          -0.890218794345856
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          0.940601587295532, -0.735241591930389,
                          0.795987248420715, -1.64818048477173,
                          -1.59416496753693, -1.56075155735016
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.926958680152893, -0.636192202568054,
                          1.05849957466125, -2.01005935668945,
                          -1.59393537044525, -1.57439470291138
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.941129803657532, -0.735469162464142,
                          0.77988338470459, -1.63183724880219,
                          -1.59417378902435, -1.56022226810455
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 729,
              "y": 369
          },
          "position3D": {
              "x": 0.138471335172653,
              "y": -0.530602157115936,
              "z": -0.245369389653206
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103693417
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 764,
              "y": 385
          },
          "position3D": {
              "x": 0.184884011745453,
              "y": -0.551474273204803,
              "z": -0.249482437968254
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103697418
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.61137187480927, -1.25921702384949, 1.89846193790436,
                          -2.20854544639587, -1.59945023059845,
                          -0.889765322208405
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.60126233100891, -0.98144519329071, 2.02839016914368,
                          -2.61653661727905, -1.59945809841156,
                          -0.899878084659576
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.61091816425323, -1.24943101406097, 1.907799243927,
                          -2.22767972946167, -1.59945380687714,
                          -0.890218794345856
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.69207000732422, -1.24200880527496, 1.73609209060669,
                          -2.06107926368713, -1.59922957420349,
                          -0.809034585952759
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.68444919586182, -0.997900426387787,
                          1.91100597381592, -2.48031854629517,
                          -1.59925723075867, -0.81665700674057
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.6923691034317, -1.24819874763489, 1.72606027126312,
                          -2.04484915733337, -1.59922885894775,
                          -0.808734476566315
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 328,
              "y": 392
          },
          "position3D": {
              "x": -0.377732485532761,
              "y": -0.585610866546631,
              "z": -0.197981551289558
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103698419
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 803,
              "y": 384
          },
          "position3D": {
              "x": 0.237438723444939,
              "y": -0.548923969268799,
              "z": -0.247559368610382
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103700417
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          0.831574499607086, -1.02994608879089,
                          1.41802561283112, -1.97796297073364,
                          -1.59222114086151, -1.66978859901428
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.814214468002319, -0.847420752048492,
                          1.57047188282013, -2.31330037117004,
                          -1.59188151359558, -1.68714833259583
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.83078396320343, -1.02392888069153, 1.42844784259796,
                          -1.99442005157471, -1.59220933914185,
                          -1.67057883739471
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78046798706055, -1.20655131340027, 1.67962777614594,
                          -2.03757643699646, -1.59878301620483,
                          -0.720602571964264
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.77480792999268, -0.974478363990784,
                          1.85620009899139, -2.44638061523438,
                          -1.59881770610809, -0.726263165473938
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.78069257736206, -1.21239256858826, 1.6695237159729,
                          -2.02162504196167, -1.59878194332123,
                          -0.720376968383789
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 842,
              "y": 357
          },
          "position3D": {
              "x": 0.286968976259232,
              "y": -0.516578435897827,
              "z": -0.226889878511429
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103709423
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 383,
              "y": 382
          },
          "position3D": {
              "x": -0.323700249195099,
              "y": -0.561988234519959,
              "z": -0.228996276855469
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103711422
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.8737518787384, -1.19074749946594, 1.74041903018951,
                          -2.11158919334412, -1.59808135032654,
                          -0.627285659313202
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.86980664730072, -0.956851005554199,
                          1.88704562187195, -2.49222254753113,
                          -1.59811091423035, -0.631231307983398
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.87357497215271, -1.182732462883, 1.75042545795441,
                          -2.12961268424988, -1.5980851650238,
                          -0.627462148666382
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          0.872950196266174, -1.14944660663605,
                          1.55096983909607, -1.99049985408783, -1.5929868221283,
                          -1.62841022014618
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.855058193206787, -0.938684225082397,
                          1.72594058513641, -2.37662672996521,
                          -1.59265756607056, -1.64630198478699
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.873641192913055, -1.15471172332764,
                          1.54088842868805, -1.97513842582703,
                          -1.59299945831299, -1.62771821022034
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 811,
              "y": 356
          },
          "position3D": {
              "x": 0.250691384077072,
              "y": -0.511406362056732,
              "z": -0.242474108934402
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103713426
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 373,
              "y": 464
          },
          "position3D": {
              "x": -0.305789798498154,
              "y": -0.676103115081787,
              "z": -0.197915434837341
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103714423
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.81600844860077, -1.21540582180023, 1.82456588745117,
                          -2.17266750335693, -1.59854829311371,
                          -0.685049116611481
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.81064009666443, -0.95660674571991, 1.95713341236115,
                          -2.56418561935425, -1.59858155250549,
                          -0.690418541431427
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.81576764583588, -1.20631861686707, 1.83397102355957,
                          -2.19116401672363, -1.59855246543884,
                          -0.685289442539215
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          0.993494033813477, -0.947554111480713,
                          1.15075647830963, -1.7893785238266, -1.59501194953918,
                          -1.50785088539124
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.978846430778503, -0.807989895343781,
                          1.37541663646698, -2.15395569801331,
                          -1.59478354454041, -1.52249944210052
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.994060635566711, -0.950043320655823,
                          1.13803601264954, -1.77415561676025,
                          -1.59502077102661, -1.50728321075439
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 755,
              "y": 349
          },
          "position3D": {
              "x": 0.174911916255951,
              "y": -0.500533521175385,
              "z": -0.24486880004406
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103720433
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 341,
              "y": 412
          },
          "position3D": {
              "x": -0.344647198915482,
              "y": -0.61808979511261,
              "z": -0.173773527145386
          },
          "quaternion3D": {
              "x": -0.430511087179184,
              "y": 0.90258526802063,
              "z": 1.88182394111891E-08,
              "w": 3.94532548853022E-08
          },
          "tags": ["manual"],
          "userTS": 1651103723426
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          1.68345272541046, -1.29541909694672, 1.94661843776703,
                          -2.21843957901001, -1.59926807880402,
                          -0.817655265331268
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.67459321022034, -1.00613808631897, 2.07925152778625,
                          -2.6406078338623, -1.59929275512695,
                          -0.826517403125763
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.68305563926697, -1.28528463840485, 1.95611727237701,
                          -2.23808193206787, -1.59927225112915,
                          -0.818051993846893
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          0.901800453662872, -1.05056595802307,
                          1.25312232971191, -1.79088521003723,
                          -1.59350204467773, -1.59955728054047
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.885673820972443, -0.910577416419983,
                          1.49177372455597, -2.16988897323608,
                          -1.59321582317352, -1.61568403244019
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.902423799037933, -1.05302095413208,
                          1.24011266231537, -1.77540695667267,
                          -1.59351301193237, -1.5989328622818
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
      (calibration, actionset, "Kit", ({
          "label": "Kit",
          "pose2D": {
              "x": 323,
              "y": 337
          },
          "position3D": {
              "x": -0.387444227933884,
              "y": -0.519102215766907,
              "z": -0.177713513374329
          },
          "quaternion3D": {
              "x": 4.2069427053093E-08,
              "y": 1,
              "z": -1.77635662764201E-15,
              "w": 6.46483044874913E-08
          },
          "tags": ["manual"],
          "userTS": 1651102529978
      }, {
          "label": "Kit",
          "pose2D": {
              "x": 755,
              "y": 359
          },
          "position3D": {
              "x": 0.173772990703583,
              "y": -0.514993786811829,
              "z": -0.24645522236824
          },
          "quaternion3D": {
              "x": 4.2069427053093E-08,
              "y": 1,
              "z": -1.77635662764201E-15,
              "w": 6.46483044874913E-08
          },
          "tags": ["manual"],
          "userTS": 1651102531975
      }), {
          "commands": [{
              "acquireImage": {
                  "tag": "tag-a-1",
                  "deviceType": "depth-camera",
                  "mode": 2
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.2163599729538, -1.47680175304413, 1.88267076015472,
                          -1.95631444454193, -1.58774507045746,
                          -0.432110249996185
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }, {
                      "rotation": [
                          0.747868895530701, -1.12671732902527,
                          1.50663924217224, -1.94846022129059,
                          -1.59940016269684, -0.86313933134079
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.739854633808136, -0.95473325252533,
                          1.69797909259796, -2.31201481819153,
                          -1.59941160678864, -0.871155798435211
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{
                      "intValue": 1
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          0.747507989406586, -1.12147271633148,
                          1.51877295970917, -1.96584677696228,
                          -1.59940385818481, -0.863499999046326
                      ],
                      "blendRadius": 0.0199999995529652,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.65078973770142, -1.31937277317047, 1.82616460323334,
                          -2.05373573303223, -1.58673357963562,
                          0.0399394147098064
                      ],
                      "blendRadius": 0.009999999776482582,
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.66125977039337, -1.05512166023254, 2.00028204917908,
                          -2.49193930625916, -1.58648288249969,
                          0.050409197807312
                      ],
                      "velocity": 0.100000001490116,
                      "acceleration": 0.200000002980232
                  }]
              }
          }, {
              "setOutput": {
                  "type": "vacuum",
                  "args": [{}]
              }
          }, {
              "movelPath": {
                  "waypoints": [{
                      "rotation": [
                          1.65040123462677, -1.32609128952026, 1.81614828109741,
                          -2.03700709342957, -1.58674335479736,
                          0.0395519211888313
                      ],
                      "velocity": 1,
                      "acceleration": 0.899999976158142
                  }]
              }
          }, {
              "movejPath": {
                  "waypoints": [{
                      "rotation": [
                          1.20381903648376, -1.53430807590485, 1.99544441699982,
                          -2.08861255645752, -1.59846460819244,
                          -0.399771809577942
                      ],
                      "velocity": 1.79999995231628,
                      "acceleration": 1.20000004768372
                  }]
              }
          }, {
              "setOutput": {
                  "type": "point-reached",
                  "name": "place-point",
                  "args": [{}]
              }
          }],
          "calibrationRequirement": {}
      }),
  )
