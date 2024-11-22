#include "energy-buffer.h"

EnergyBuffer::EnergyBuffer(double initialEnergy, double capacity)
    : energyAmount(initialEnergy), maxEnergy(capacity) {}

bool EnergyBuffer::consumeEnergy(double amount) {
    if (energyAmount >= amount) {
        energyAmount -= amount;
        return true;
    }
    energyAmount = 0;
    return false;
}

void EnergyBuffer::recharge(double amount) {
    energyAmount += amount;
    if (energyAmount > maxEnergy) {
        energyAmount = maxEnergy;
    }
}

bool EnergyBuffer::hasEnergy() const {
    return energyAmount > 0;
}

double EnergyBuffer::getEnergyAmount() const {
    return energyAmount;
}

void EnergyBuffer::setMaxEnergy(double capacity) {
    maxEnergy = capacity;
}