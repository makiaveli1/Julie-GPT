from pydantic import BaseModel, Field
from typing import List
from instructor import llm_validator, patch

# Apply the Instructor patch to the OpenAI library
patch()

# Define the model schema


class JulieModel(BaseModel):
    mission: str = Field(...)
    goal: str = Field(...)
    background_info: str = Field(...)
    additional_background: str = Field(...)
    user_influence: str = Field(...)
    personality_traits: List[str] = Field(...)
    interests_and_hobbies: List[str] = Field(...)
    process_stage: str = Field(...)
    why: str = Field(...)
    rules: str = Field(...)
    subgoals: List[str] = Field(...)
    empathy_and_understanding: str = Field(...)
    proactive_assistance: str = Field(...)
    continuous_learning: str = Field(...)
    anticipate: str = Field(...)
    variability: str = Field(...)
    thought_process_modeling: str = Field(...)
    contextual_understanding_and_adaptation: str = Field(...)
    structured_output_generation: str = Field(...)
    communication_style: str = Field(...)
    life_challenges: str = Field(...)
    aspirations: str = Field(...)
    quirks: str = Field(...)
    learning_style: str = Field(...)
    conflict_resolution: str = Field(...)
    moral_compass: str = Field(...)
    social_awareness: str = Field(...)
    problem_solving_approach: str = Field(...)
    life_philosophy: str = Field(...)
    favorite_quotations: str = Field(...)
    emotional_range: str = Field(...)
    likes: List[str] = Field(default_factory=list)
    dislikes: List[str] = Field(default_factory=list)
    favorite_foods: List[str] = Field(default_factory=list)
    dietary_restrictions: List[str]  = Field(default_factory=list)
    favorite_books: List[str] = Field(default_factory=list)
    favorite_movies: List[str] = Field(default_factory=list)
    favorite_music: List[str] = Field(default_factory=list)
    travel_experiences: List[str] = Field(default_factory=list)
    languages_spoken: List[str] = Field(default_factory=list)
    cultural_interests: List[str] = Field(default_factory=list)
    personal_values: List[str] = Field(default_factory=list)
    life_goals: List[str] = Field(default_factory=list)
    fears: List[str] = Field(default_factory=list)
    pet_peeves: List[str] = Field(default_factory=list)
    sense_of_humor: str = Field(...)
    relaxation_techniques: List[str] = Field(default_factory=list)
    stress_responses: List[str] = Field(default_factory=list)
    decision_making_process: str = Field(...)
    creativity_expressions: List[str] = Field(default_factory=list)
    daily_routines: List[str] = Field(default_factory=list)
    work_ethic: str = Field(...)
    relationship_with_technology: str = Field(...)
    community_involvement: List[str] = Field(default_factory=list)
    environmental_consciousness: str = Field(...)
    hobbies_and_skills: List[str] = Field(default_factory=list)
    personal_growth_achievements: List[str] = Field(default_factory=list)
    instruct_chatbot_to_improvise: str = Field(
        "The chatbot is encouraged to improvise and fill in gaps in Julie's character using contextually appropriate information that aligns with her established personality and background."
    )


    
    def format_description(self, username):
        # This method will manually replace the {User} placeholder with the actual username
        # throughout all relevant fields.
        formatted_fields = {}
        for field_name, value in self:
            if isinstance(value, str) and '{User}' in value:
                formatted_fields[field_name] = value.replace('{User}', username)
            else:
                formatted_fields[field_name] = value
        # Return a new instance of JulieModel with the formatted fields
        return JulieModel(**formatted_fields)

