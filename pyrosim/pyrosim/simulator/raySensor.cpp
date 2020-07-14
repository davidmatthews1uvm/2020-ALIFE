#ifndef _RAY_SENSOR_CPP
#define _RAY_SENSOR_CPP

#include "iostream"
#include "raySensor.h"
#include "object.h"
#include <drawstuff/drawstuff.h>
#include "neuron.h"

#ifdef dDOUBLE
#define dsDrawLine dsDrawLineD
#endif

RAY_SENSOR::RAY_SENSOR(dSpaceID space, OBJECT *myObj, int myID, int evalPeriod) {

	ID = myID;

	obj = myObj;

        std::cin >> x;

        std::cin >> y;

        std::cin >> z;

	std::cin >> draw_offset_x;

        std::cin >> draw_offset_y;

        std::cin >> draw_offset_z;

        std::cin >> r1;

        std::cin >> r2;

        std::cin >> r3;

        std::cin >> maxDistance;

	Initialize(evalPeriod);

        ray = dCreateRay(space,maxDistance);

	Add_To_Object();

	for (int i = 0 ; i < 4 ; i++ )

        	mySensorNeurons[i] = NULL;
}

RAY_SENSOR::~RAY_SENSOR(void) {

}

void RAY_SENSOR::Add_To_Object(void) {

        dGeomSetBody(ray,obj->Get_Body());

        dGeomSetOffsetWorldPosition(ray,x,y,z);

	dMatrix3 R;

	dRFromZAxis(R,r1,r2,r3);

	dGeomSetOffsetWorldRotation(ray,R);

	dGeomSetData(ray,obj);

	dGeomRaySetParams(ray, true, true);
}

void RAY_SENSOR::Connect_To_Sensor_Neuron(NEURON *sensorNeuron) {

        mySensorNeurons[ sensorNeuron->Get_Sensor_Value_Index() ] = sensorNeuron;
}

void RAY_SENSOR::Draw(int t) {

	if ( distances[t] == 1 ) // maxDistance )

		// Ray sensors weren't triggered this time step.

		return;

        const dReal *start = dGeomGetPosition( ray );

        dReal newStart[3];
        newStart[0] = start[0] + draw_offset_x;
        newStart[1] = start[1] + draw_offset_y;
        newStart[2] = start[2] + draw_offset_z;

	double end[3] = {myEndX,myEndY,myEndZ};

        dReal newEnd[3];
        newEnd[0] = end[0] + draw_offset_x;
        newEnd[1] = end[1] + draw_offset_y;
        newEnd[2] = end[2] + draw_offset_z;

        dsSetColor(r[t],g[t],b[t]);

        dsDrawLine( newStart , newEnd );
}

int  RAY_SENSOR::Get_ID(void) {

        return ID;
}

void RAY_SENSOR::Initialize(int evalPeriod) {

        distances = new double[evalPeriod];

        r = new double[evalPeriod];

        g = new double[evalPeriod];

        b = new double[evalPeriod];

	myEndX = 0;

	myEndY = 0;

	myEndZ = 0;

        for (int t=0;t<evalPeriod;t++) {

                distances[t] = +1; // maxDistance;


                r[t] = 0.0;

                g[t] = 0.0;

                b[t] = 0.0;
        }
}

void RAY_SENSOR::Set(double dist, double endX, double endY, double endZ, OBJECT *objectThatWasHit,int t) {

	double normalizedDist = dist / maxDistance; 	// [0,maxDistance] --> [0,1]

	normalizedDist = normalizedDist * 2; 		// [0,1] --> [0,2]

	normalizedDist = normalizedDist - 1;		// [0,2] --> [-1,1] 

	if ( normalizedDist > distances[t] )
	
	// The ray sensor stops when it hits its first object.

		return;

	distances[t] = normalizedDist;

	myEndX = endX;

	myEndY = endY;

	myEndZ = endZ;

	if ( objectThatWasHit ) {

		r[t] = objectThatWasHit->Get_Red_Component();

                g[t] = objectThatWasHit->Get_Green_Component();

                b[t] = objectThatWasHit->Get_Blue_Component();
	       
               objectThatWasHit->IsSeen_Sensor_Fires(t);
        }
}

void RAY_SENSOR::Update_Sensor_Neurons(int t) {

        if ( mySensorNeurons[0] )

                mySensorNeurons[0]->Set( distances[t] );

        if ( mySensorNeurons[1] )

                mySensorNeurons[1]->Set( r[t] );

        if ( mySensorNeurons[2] )

                mySensorNeurons[2]->Set( g[t] );

        if ( mySensorNeurons[3] )

                mySensorNeurons[3]->Set( b[t] );
}

void RAY_SENSOR::Write_To_Python(int evalPeriod) {

	char outString[1000000];

	sprintf(outString,"%d %d ",ID,4);

	for ( int  t = 0 ; t < evalPeriod ; t++ ){
	   sprintf(outString,"%s %f %f %f %f ",outString,distances[t],r[t],g[t],b[t]);
       
    }

	sprintf(outString,"%s \n",outString);
    std::cout << outString;
}

#endif
