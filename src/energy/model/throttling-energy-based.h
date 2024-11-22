#ifndef ENERGY_BASED_THROTTLING_H
#define ENERGY_BASED_THROTTLING_H

#include "ns3/core-module.h"

namespace ns3
{

enum class ThrottlingMode
{
    NORMAL,
    CONSERVATIVE,
    CRITICAL,
    SLEEP
};

class EnergyBasedThrottling
{
  public:
    EnergyBasedThrottling(double bufferSize);

    /**
     * Define o nível de energia atual e ajusta o modo de throttling conforme necessário.
     * @param currentEnergy Energia restante no buffer.
     */
    void updateEnergyLevel(double currentEnergy);

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
    int m_availableTokens;           // Tokens disponíveis para requisições
    Time m_lastTime;                 // Último tempo de verificação
    ThrottlingMode m_throttlingMode; // Modo de throttling atual
    int tot_denied;
    int getMaxRequestsPerSecond() const; // Obtém o limite de requisições com base no modo
};

} // namespace ns3

#endif
