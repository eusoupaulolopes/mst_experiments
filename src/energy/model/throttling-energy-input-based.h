#ifndef ENERGY_INPUT_BASED_THROTTLING_H
#define ENERGY_INPUT_BASED_THROTTLING_H

#include "ns3/core-module.h"

namespace ns3
{



class EnergyInputBasedThrottling
{
  public:
    EnergyInputBasedThrottling(double bufferSize,  double recoveryRate);

    /**
     * Define o nível de energia atual e ajusta o modo de throttling conforme necessário.
     * @param currentEnergy Energia restante no buffer.
     */
    void updateEnergyLevel(double energyInput);

    /**
     * Informa o valor de energia coletado e ajusta o modo de throttling conforme necessário.
     * @param currentInput Energia restante no buffer.
     */
    void updateLastEnergyInput(double currentInput);

      /**
     * Informa o valor de custo por operação.
     * @param currentInput Energia restante no buffer.
     */
    void updateOperationCost(double currentInput);

    /**
     * Verifica se uma requisição pode ser processada de acordo com o modo de throttling atual.
     * @return True se a requisição pode ser processada; caso contrário, False.
     */
    bool canProceed();

    /**
     * Verifica modo de Throttle atual.
     * @return NORMAL, CONSERVATIVE, CRITICAL, SLEEP.
     */
    std::string getThrottleMode();

    int getTotalthrottled();

  private:
    void updateThrottlingMode();

    double m_bufferSize;             // Capacidade total do buffer energético
    double m_currentEnergy;          // Energia atual no buffer
    double recoveryRate;             // Rate de recuperação energética em SLEEP   
    double m_energyInput;         
    int m_availableTokens;           // Tokens disponíveis para requisições
    Time m_lastTime;                 // Último tempo de verificação
    ThrottlingMode m_throttlingMode; // Modo de throttling atual
    int tot_denied;
    int getMaxRequestsPerSecond() const; // Obtém o limite de requisições com base no modo
    double getMaxRequestsPerSecondByHarvest() const;
};

} // namespace ns3

#endif
