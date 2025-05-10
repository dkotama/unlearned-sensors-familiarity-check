from pydantic import BaseModel, Field, validator
from typing import Union, Literal, Optional

class ReviewChunk1(BaseModel):
    """First chunk: P1-P6 criteria"""
    sensor_evaluated: str
    p1_score: Union[int, Literal["N/A"]] = Field(description="Disclaimer section score")
    p1_justification: str
    p2_score: Union[int, Literal["N/A"]] = Field(description="Manufacturer info score")
    p2_justification: str
    p3_score: Union[int, Literal["N/A"]] = Field(description="General description score")
    p3_justification: str
    p4_score: Union[int, Literal["N/A"]] = Field(description="Theory of operation score")
    p4_justification: str
    p5_score: Union[int, Literal["N/A"]] = Field(description="Features score")
    p5_justification: str
    p6_score: Union[int, Literal["N/A"]] = Field(description="Potential applications score")
    p6_justification: str

class ReviewChunk2(BaseModel):
    """Second chunk: P7-P11 criteria"""
    sensor_evaluated: str
    p7_score: Union[int, Literal["N/A"]] = Field(description="Pin configuration score")
    p7_justification: str
    p8_score: Union[int, Literal["N/A"]] = Field(description="Absolute maximum ratings score")
    p8_justification: str
    p9_score: Union[int, Literal["N/A"]] = Field(description="Electrical characteristics score")
    p9_justification: str
    p10_score: Union[int, Literal["N/A"]] = Field(description="Operating conditions score")
    p10_justification: str
    p11_score: Union[int, Literal["N/A"]] = Field(description="Sensor performance score")
    p11_justification: str

class ReviewChunk3(BaseModel):
    """Third chunk: P12-P16 criteria and overall score"""
    sensor_evaluated: str
    p12_score: Union[int, Literal["N/A"]] = Field(description="Communication protocol score")
    p12_justification: str
    p13_score: Union[int, Literal["N/A"]] = Field(description="Register map score")
    p13_justification: str
    p14_score: Union[int, Literal["N/A"]] = Field(description="Package information score")
    p14_justification: str
    p15_score: Union[int, Literal["N/A"]] = Field(description="Basic usage score")
    p15_justification: str
    p16_score: Union[int, Literal["N/A"]] = Field(description="Compliance score")
    p16_justification: str
    overall_score: int = Field(ge=1, le=5, description="Overall evaluation score")
    overall_justification: str
    confirmation: str

class CompleteReview(BaseModel):
    """Complete review combining all chunks"""
    sensor_evaluated: str
    p1_score: Union[int, Literal["N/A"]]
    p1_justification: str
    p2_score: Union[int, Literal["N/A"]]
    p2_justification: str
    p3_score: Union[int, Literal["N/A"]]
    p3_justification: str
    p4_score: Union[int, Literal["N/A"]]
    p4_justification: str
    p5_score: Union[int, Literal["N/A"]]
    p5_justification: str
    p6_score: Union[int, Literal["N/A"]]
    p6_justification: str
    p7_score: Union[int, Literal["N/A"]]
    p7_justification: str
    p8_score: Union[int, Literal["N/A"]]
    p8_justification: str
    p9_score: Union[int, Literal["N/A"]]
    p9_justification: str
    p10_score: Union[int, Literal["N/A"]]
    p10_justification: str
    p11_score: Union[int, Literal["N/A"]]
    p11_justification: str
    p12_score: Union[int, Literal["N/A"]]
    p12_justification: str
    p13_score: Union[int, Literal["N/A"]]
    p13_justification: str
    p14_score: Union[int, Literal["N/A"]]
    p14_justification: str
    p15_score: Union[int, Literal["N/A"]]
    p15_justification: str
    p16_score: Union[int, Literal["N/A"]]
    p16_justification: str
    overall_score: int
    overall_justification: str
    confirmation: str
    
    @validator('p1_score', 'p2_score', 'p3_score', 'p4_score', 'p5_score', 'p6_score', 
               'p7_score', 'p8_score', 'p9_score', 'p10_score', 'p11_score', 
               'p12_score', 'p13_score', 'p14_score', 'p15_score', 'p16_score')
    def validate_scores(cls, v):
        if isinstance(v, int) and not (1 <= v <= 5):
            raise ValueError("Score must be between 1 and 5 if numeric")
        return v