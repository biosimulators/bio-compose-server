# -- gateway models -- #
# -- worker models -- #
import os
from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import *

from dotenv import load_dotenv
from pydantic import Field, BaseModel as _BaseModel, ConfigDict
from fastapi.responses import FileResponse
import numpy as np


class BaseModel(_BaseModel):
    """Base Pydantic Model with custom app configuration"""
    model_config = ConfigDict(arbitrary_types_allowed=True)


@dataclass
class BaseClass:
    """Base Python Dataclass multipurpose class with custom app configuration."""
    def to_dict(self):
        return asdict(self)

    def serialize(self):
        return asdict(self)


# -- requests --

@dataclass
class Run(BaseClass):
    job_id: str
    last_updated: str
    status: str


@dataclass
class CompositionRun(Run):
    simulators: List[str]
    duration: int
    spec: Dict[str, Any]
    results: Dict[str, Any] = field(default=None)


@dataclass
class SmoldynRun(Run):
    path: str
    duration: float
    dt: float


@dataclass
class UtcRun(Run):
    simulator: str
    model_file: str
    start: int
    stop: int
    steps: int
    params: Dict[str, Any] = field(default=None)


@dataclass
class AmiciRun(UtcRun):
    pass


@dataclass
class CobraRun(UtcRun):
    pass


@dataclass
class CopasiRun(UtcRun):
    pass


@dataclass
class TelluriumRun(UtcRun):
    pass


@dataclass
class ReaddySpeciesConfig(BaseClass):
    name: str
    diffusion_constant: float


@dataclass
class ReaddyReactionConfig(BaseClass):
    scheme: str
    rate: float


@dataclass
class ReaddyParticleConfig(BaseClass):
    name: str
    initial_positions: List[List[float]]


@dataclass
class ReaddyRun(Run):
    duration: float
    dt: float
    box_size: List[float]
    species_config: Union[Dict[str, float], List[ReaddySpeciesConfig]]
    particles_config: Union[Dict[str, List[List[float]]], List[ReaddyParticleConfig]]
    reactions_config: Union[Dict[str, float], List[ReaddyReactionConfig]]
    unit_system_config: Dict[str, Any]
    reaction_handler: str


@dataclass
class SimulariumAgentParameter(BaseClass):
    name: str
    radius: Optional[float]
    mass: Optional[float]
    density: Optional[float]


@dataclass
class SimulariumAgentParameters(BaseClass):
    agents: List[SimulariumAgentParameter]


@dataclass
class DbClientResponse(BaseClass):
    message: str
    db_type: str  # ie: 'mongo', 'postgres', etc
    timestamp: str
    status: str = field(default=None)  # either PASS or FAIL


# -- process-bigraph specs --

@dataclass
class BigraphRegistryAddresses(BaseClass):
    version: str
    registered_addresses: List[str]


class DataStorePath(str):
    pass


@dataclass
class DataStore(BaseClass):
    paths: List[DataStorePath | str] | str

    def __post_init__(self):
        if isinstance(self.paths, str):
            self.paths = [DataStorePath(self.paths)]
        else:
            paths = {
                path_i: path for path_i, path in enumerate(self.paths)
            }
            for i, path in paths.items():
                if isinstance(path, str):
                    paths[i] = DataStorePath(path)
            self.paths = list(paths.values())


@dataclass
class PortStore(BaseClass):
    name: str  # outermost keys under "inputs"
    store: DataStore | List[str]  # ie: ["concentrations_store"]

    def __post_init__(self):
        if isinstance(self.store, list):
            self.store = DataStore(self.store)


@dataclass
class CompositionNode(BaseClass):
    name: str
    _type: str
    address: str
    config: Dict[str, Any]
    inputs: Dict[str, List[str]]
    outputs: Optional[Dict[str, List[str]]] = None

    def to_dict(self):
        rep = super().to_dict()
        rep.pop("name")
        if not self.outputs:
            rep.pop("outputs")
        return rep


@dataclass
class CompositionSpec(BaseClass):
    """To be used as input to process_bigraph.Composition() like:

        spec = CompositionSpec(nodes=nodes, emitter_mode='ports')
        composite = Composition({'state': spec
    """
    nodes: List[CompositionNode]
    job_id: str
    emitter_mode: str = "all"

    @property
    def spec(self):
        return {
            node_spec.name: node_spec.to_dict()
            for node_spec in self.nodes
        }


# -- output data/responses --

@dataclass
class OutputData(BaseClass):
    job_id: str
    status: str
    last_updated: str
    results: Dict


class SmoldynOutput(FileResponse):
    pass


@dataclass
class ValidatedComposition(BaseClass):
    valid: bool
    invalid_nodes: Dict[str, str]


@dataclass
class OutputFile(BaseClass):
    results_file: str


# -- misc --

@dataclass
class HealthCheckResponse(BaseClass):
    version: str
    status: str
    message: str = field(default="Welcome to the BioCompose API")
    swagger_ui: str = field(default="https://compose.biosimulations.org/docs")


@dataclass
class IncompleteFileJob(BaseClass):
    job_id: str
    timestamp: float
    status: str
    source: str


class JobStatuses:
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


APP_SERVERS = [
    # {
    #     "url": "https://compose.biosimulations.org",
    #     "description": "Production server"
    # },
    # {
    #     "url": "http://localhost:3001",
    #     "description": "Main Development server"
    # },
    # {
    #     "url": "http://localhost:8000",
    #     "description": "Alternate Development server"
    # }
]



