#ifndef _RAY_SENSOR_H
#define _RAY_SENSOR_H

#include <ode/ode.h>

class OBJECT;

class NEURON;

class RAY_SENSOR {

private:
	int ID;

	double *distances;

	OBJECT *obj;

        dGeomID ray;

	double x, y, z;

	double draw_offset_x;
        double draw_offset_y;
        double draw_offset_z;

	double r1,r2,r3;

	double *r, *g, *b;

	double myEndX, myEndY, myEndZ;

    double maxDistance;

    NEURON *mySensorNeurons[4];

public:
	RAY_SENSOR(dSpaceID space, OBJECT *myObj, int myID, int evalPeriod);

	~RAY_SENSOR(void);

	void Add_To_Object(void);

    void Connect_To_Sensor_Neuron(NEURON *sensorNeuron);

	void Draw(int t);

        int  Get_ID(void);

	void Initialize(int evalPeriod);

	void Reset(void);

	void Set(double distance, double endX, double endY, double endZ, OBJECT *objectThatWasHit, int t);

        void Update_Sensor_Neurons(int t);

	void Write_To_Python(int evalPeriod);
};

#endif
