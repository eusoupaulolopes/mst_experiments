// EnergyBuffer.h

#ifndef ENERGYBUFFER_H
#define ENERGYBUFFER_H

class EnergyBuffer {
private:
    double energyAmount;
    double maxEnergy;

public:
    // Construtor
    EnergyBuffer(double initialEnergy, double capacity);

    // Métodos
    bool consumeEnergy(double amount);
    void recharge(double amount);
    bool hasEnergy() const;
    double getEnergyAmount() const;
    void setMaxEnergy(double capacity);
};

#endif // ENERGYBUFFER_H