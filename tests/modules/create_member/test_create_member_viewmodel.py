from src.modules.create_member.app.create_member_viewmodel import CreateMemberViewModel
from src.shared.domain.entities.member import Member


class Test_CreateMemberViewModel:
    def test_create_member_viewmodel(self):
        member = Member(
            member_id='f4019bd7-52d3-463d-8ab1-1d373c004a43',
            member_photo='https://picsum.photos/800/600.jpg',
            member_name='nome_membro',
            member_intro='intro_membro'
        )

        viewmodel = CreateMemberViewModel(member)

        response = viewmodel.to_dict()

        assert response == {
            'member_id': str(member.member_id),
            'member_photo': str(member.member_photo),
            'member_name': 'nome_membro',
            'member_intro': 'intro_membro',
            'message': 'the member was created succefully'
        }
