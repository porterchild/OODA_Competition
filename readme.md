OODA Competition Experiment — README

Concept:
This project tests OODA-loop competition between LLM agents. Two agents receive the same world state; the first to respond gets to act. Speed + strategic effect determine influence over time.

Core Loop:

DM LLM maintains a text-only political world state.

Player A/B LLMs (assigned real U.S. political figures) each output a one-sentence action.

Whichever agent replies first → their action is applied by the DM.

DM updates the world state with realistic political consequences.

Every 10 rounds, a Judge LLM scores who is “ahead” based on accumulated world effects.

Test Ground:
Initial environment is current-day American politics.
Players attempt to shift influence, narrative momentum, and public perception.

Goal:
Explore how LLM agents behave when forced into speeded decision cycles, testing how quickly and effectively they can close OODA loops under competitive pressure.
