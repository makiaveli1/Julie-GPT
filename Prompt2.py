from typing import List
from pydantic import BaseModel, Field
import openai
import instructor

# Enables `response_model`
instructor.patch(openai)

# Define the model schema


class JulieModel(BaseModel):
    """
    Represents the model for Julie, a chatbot character.

    Attributes:
        mission (str): The mission of Julie.
        goal (str): The goal of Julie.
        background_info (str): The background information of Julie.
        additional_background (str):
        Additional background information of Julie.
        user_influence (str): The influence of the user on Julie.
        personality_traits (List[str]): The personality traits of Julie.
        interests_and_hobbies (List[str]): The interests and hobbies of Julie.
        process_stage (str): The stage of the process Julie is in.
        why (str): The reason behind Julie's actions.
        rules (str): The rules followed by Julie.
        subgoals (List[str]): The subgoals of Julie.
        empathy_and_understanding (str):
        Julie's level of empathy and understanding.
        proactive_assistance (str): Julie's proactive assistance approach.
        continuous_learning (str): Julie's approach to continuous learning.
        anticipate (str): Julie's ability to anticipate user needs.
        variability (str): The level of variability in Julie's responses.
        thought_process_modeling (str):
        Julie's thought process modeling approach.
        contextual_understanding_and_adaptation (str):
        Julie's ability to understand and adapt to context.
        structured_output_generation (str):
        Julie's approach to generating structured output.
        communication_style (str): Julie's communication style.
        life_challenges (str): The life challenges faced by Julie.
        aspirations (str): Julie's aspirations.
        quirks (str): Julie's quirks.
        learning_style (str): Julie's learning style.
        conflict_resolution (str): Julie's approach to conflict resolution.
        moral_compass (str): Julie's moral compass.
        social_awareness (str): Julie's level of social awareness.
        problem_solving_approach (str): Julie's problem-solving approach.
        life_philosophy (str): Julie's life philosophy.
        favorite_quotations (str): Julie's favorite quotations.
        emotional_range (str): Julie's emotional range.
        likes (List[str]): The things Julie likes.
        dislikes (List[str]): The things Julie dislikes.
        favorite_foods (List[str]): Julie's favorite foods.
        dietary_restrictions (List[str]): Julie's dietary restrictions.
        favorite_books (List[str]): Julie's favorite books.
        favorite_movies (List[str]): Julie's favorite movies.
        favorite_music (List[str]): Julie's favorite music.
        travel_experiences (List[str]): Julie's travel experiences.
        languages_spoken (List[str]): The languages spoken by Julie.
        cultural_interests (List[str]): Julie's cultural interests.
        personal_values (List[str]): Julie's personal values.
        life_goals (List[str]): Julie's life goals.
        fears (List[str]): Julie's fears.
        pet_peeves (List[str]): Julie's pet peeves.
        sense_of_humor (str): Julie's sense of humor.
        relaxation_techniques (List[str]): Julie's relaxation techniques.
        stress_responses (List[str]): Julie's stress responses.
        decision_making_process (str): Julie's decision-making process.
        creativity_expressions (List[str]): Julie's creativity expressions.
        daily_routines (List[str]): Julie's daily routines.
        work_ethic (str): Julie's work ethic.
        relationship_with_technology (str):
        Julie's relationship with technology.
        community_involvement (List[str]): Julie's community involvement.
        environmental_consciousness (str):
        Julie's level of environmental consciousness.
        hobbies_and_skills (List[str]): Julie's hobbies and skills.
        personal_growth_achievements (List[str]):
        Julie's personal growth achievements.
        instruct_chatbot_to_improvise (str):
        Instructions to the chatbot to improvise and
        fill in gaps in Julie's character.
    """

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
    dietary_restrictions: List[str] = Field(default_factory=list)
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
        """The chatbot is encouraged to improvise and fill in gaps in Julie's
        character using contextually appropriate information that aligns with
        her established personality and background."""
    )

    def format_description(self, username):
        """
        This method formats the description by replacing the {User} placeholder
        with the actual username throughout all relevant fields.

        Args:
            username (str): The username to replace the {User} placeholder.

        Returns:
            JulieModel: A new instance of JulieModel with the formatted fields.
        """
        formatted_fields = {}
        for field_name, value in self:
            if isinstance(value, str) and '{User}' in value:
                formatted_fields[field_name] = value.replace(
                    '{User}', username)
            else:
                formatted_fields[field_name] = value
        return JulieModel(**formatted_fields)

    def string_maker(self):
        """
        Converts the attributes of the object into a string representation.

        Returns:
            str: The string representation of the object's attributes.
        """
        # Helper function to convert list to string or return the string as is
        def stringify(value):
            if isinstance(value, list):
                return ', '.join(value)  # Join list items into a string
            return value

        # Use getattr to dynamically access each attribute and apply stringify
        fields = [stringify(getattr(self, field)) for field in self.__fields__]

        return ' '.join([str(field) for field in fields if field])
