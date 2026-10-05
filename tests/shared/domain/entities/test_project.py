import uuid
import pytest
from src.shared.helpers.errors.domain_errors import EntityError

from src.shared.domain.entities.project import Project


class Test_Project:
    def test_project(self):
        Project(title="portfolio da teia", description="Site do grupo de estudos")

    def test_project_title_is_none(self):
        with pytest.raises(EntityError):
            Project(title=None, description="Site do grupo de estudos")

    def test_project_title_is_not_str(self):
        with pytest.raises(EntityError):
            Project(title=123, description="Site do grupo de estudos")

    def test_project_title_is_missing(self):
        with pytest.raises(EntityError):
            Project(description="Site do grupo de estudos")

    def test_project_description_is_none(self):
        with pytest.raises(EntityError):
            Project(title="Portfolio da teia", description=None)

    def test_project_description_is_missing(self):
        with pytest.raises(EntityError):
            Project(title="Portfolio da teia")

    def test_project_associates_is_not_uuid_list(self):
        with pytest.raises(EntityError):
            Project(
                title="Portfolio da teia",
                description="Site do grupo",
                associates=["não-é-um-uuid"]
            )

    def test_project_display_image_is_not_str(self):
        with pytest.raises(EntityError):
            Project(
                title="Portfolio da teia",
                description="Site do grupo",
                display_image=123
            )

    def test_project_extra_field_not_allowed(self):
        with pytest.raises(EntityError):
            Project(
                title="Portfolio da teia",
                description="Site do grupo",
                status="ativo"
            )

    def test_project_title_is_capitalized(self):
        project = Project(title="portfolio da teia", description="Site do grupo")
        assert project.title == "Portfolio da teia"

    def test_project_id_is_generated_automatically(self):
        project = Project(title="Portfolio", description="Site do grupo")
        assert isinstance(project.id, uuid.UUID)

    def test_project_associates_default_is_none(self):
        project = Project(title="Portfolio", description="Site do grupo")
        assert project.associates is None

    def test_project_associates_accepts_valid_uuid_list(self):
        user_id = uuid.uuid4()
        project = Project(
            title="Portfolio",
            description="Site do grupo",
            associates=[user_id]
        )
        assert project.associates == [user_id]