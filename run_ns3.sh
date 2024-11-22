#!/bin/bash

# Nome da sessão do tmux
SESSION_NAME="ns3_sensors"

# Matar a sessão tmux existente, se houver
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Inicia uma nova sessão tmux com o nome especificado
tmux new-session -d -s $SESSION_NAME

# Primeiro comando em um pane
tmux send-keys -t $SESSION_NAME "./ns3 run Sensor1" C-m

# Segundo pane
tmux split-window -h
tmux send-keys "./ns3 run Sensor2" C-m

# Terceiro pane
tmux split-window -h
tmux send-keys "./ns3 run Sensor3" C-m


# Quarto pane
tmux split-window -h
tmux send-keys "./ns3 run Sensor4" C-m

# Alternativamente, divida verticalmente:
# tmux split-window -v

tmux select-layout -t $SESSION_NAME tiled

# Anexa à sessão para ver os comandos sendo executados
tmux attach-session -t $SESSION_NAME
