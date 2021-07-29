// Copyright 2021 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#define IKFAST_HAS_LIBRARY
#include "reachrobots/ikfast.h" // found inside share/openrave-X.Y/python/ikfast.h
using namespace ikfast;

IKFAST_API int ik(double * eetrans, double * eerot, double * result) {
    IkSolutionList<IkReal> solutions;
    std::vector<IkReal> vfree(GetNumFreeParameters());
    bool bSuccess = ComputeIk(eetrans, eerot, NULL, solutions);

    if( !bSuccess ) {
        return 0;
    }

    // does not yet support free joints
    int free_size = (int)solutions.GetSolution(0).GetFree().size();
    if (free_size != 0){
        return -1;
    }

    std::vector<IkReal> solvalues(GetNumJoints());
    for(std::size_t i = 0; i < solutions.GetNumSolutions(); ++i) {
        const IkSolutionBase<IkReal>& sol = solutions.GetSolution(i);
        std::vector<IkReal> vsolfree(sol.GetFree().size());
        sol.GetSolution(&solvalues[0],vsolfree.size()>0?&vsolfree[0]:NULL);
        for( std::size_t j = 0; j < solvalues.size(); ++j)
            result[i*solvalues.size() + j] = solvalues[j];
    }
    return solutions.GetNumSolutions();
}

IKFAST_API int InverseKinematics760(float * posquat, float * soldata, int maxSolutions) {
    IkReal eetrans[3];
    eetrans[0] = posquat[0];
    eetrans[1] = posquat[1];
    eetrans[2] = posquat[2];

    // Convert input effector pose, in w x y z quaternion notation, to rotation matrix.
    // Must use doubles, else lose precision compared to directly inputting the rotation matrix.
    double qw = posquat[3];
    double qx = posquat[4];
    double qy = posquat[5];
    double qz = posquat[6];

    const double n = 1.0f / sqrt(qx*qx + qy * qy + qz * qz + qw * qw);
    qw *= n;
    qx *= n;
    qy *= n;
    qz *= n;
    IkReal eerot[] = {
        1.0f - 2.0f*qy*qy - 2.0f*qz*qz, 2.0f*qx*qy - 2.0f*qz*qw,        2.0f*qx*qz + 2.0f*qy*qw,
        2.0f*qx*qy + 2.0f*qz*qw,        1.0f - 2.0f*qx*qx - 2.0f*qz*qz, 2.0f*qy*qz - 2.0f*qx*qw,
        2.0f*qx*qz - 2.0f*qy*qw,        2.0f*qy*qz + 2.0f*qx*qw,        1.0f - 2.0f*qx*qx - 2.0f*qy*qy
    };

    IkSolutionList<IkReal> solutions;
    std::vector<IkReal> vfree(0);
    bool success = ComputeIk(eetrans, eerot, vfree.size() > 0 ? &vfree[0] : NULL, solutions);
    if (!success) {
        return 0;
    }

    unsigned int num_of_solutions = (int)solutions.GetNumSolutions();
    std::vector<IkReal> solvalues(6);
    int counter = 0;
    for (std::size_t i = 0; i < num_of_solutions; ++i) {
        const IkSolutionBase<IkReal>& sol = solutions.GetSolution(i);
        int this_sol_free_params = (int)sol.GetFree().size();
        std::vector<IkReal> vsolfree(this_sol_free_params);

        sol.GetSolution(&solvalues[0], vsolfree.size() > 0 ? &vsolfree[0] : NULL);

        for (std::size_t j = 0; j < solvalues.size(); ++j) {
            soldata[counter] = solvalues[j];
            counter++;
        }
    }

    return num_of_solutions;
}

IKFAST_API void fk(double * j, double * eetrans, double * eerot) {
    ComputeFk(j, eetrans, eerot);
}

IKFAST_API void ForwardKinematics639(float * angles, float * pos, float * rot) {
    IkReal eerot[9], eetrans[3];
    IkReal joints[6];
    for (int i = 0; i < 6; i++) {
        joints[i] = angles[i];
    }

    ComputeFk(joints, eetrans, eerot);

    for (int i = 0; i < 3; i++) {
        pos[i] = eetrans[i];
    }

    for (int i = 0; i < 9; i++) {
        rot[i] = eerot[i];
    }
}
