#ifndef THROTTLING_STRATEGY_H
#define THROTTLING_STRATEGY_H

class ThrottlingStrategy {
public:
    virtual ~ThrottlingStrategy() = default;
    
    virtual bool canProceed() = 0;

    virtual void UpdateEnergyLevel(double currentEnergy) {};
};

#endif 