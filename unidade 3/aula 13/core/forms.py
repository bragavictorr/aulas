from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import (
    UserProfile, HiringRequest, Project, ProjectComment,
    PartnershipProposal, PartnershipMessage, UserSuggestion
)

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Usuário",
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='O nome de usuário deve conter apenas letras, números e sublinhados.'
            )
        ],
        help_text='Obrigatório. Apenas letras, números e sublinhado (_).'
    )
    
    email = forms.EmailField(required=True, label="E-mail")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'cover_image', 'especialidade', 'bio', 'portfolio_url', 'location', 'available_for_hire')
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'avatar-file-input',
                'id': 'avatarFileInput',
                'accept': 'image/*'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'avatar-file-input',
                'id': 'coverFileInput',
                'accept': 'image/*'
            }),
            'especialidade': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Animação 3D, VFX Shaders, Motion 2D'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control-art',
                'rows': 3,
                'placeholder': 'Escreva sobre suas técnicas, ferramentas (Blender, Cinema 4D, After Effects...) e experiência.'
            }),
            'portfolio_url': forms.URLInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'https://github.com/seunome ou https://behance.net/seunome'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: São Paulo, Brasil / Remoto'
            }),
            'available_for_hire': forms.CheckboxInput(attrs={
                'class': 'checkbox-art'
            }),
        }
        labels = {
            'avatar': 'Foto de Perfil (Avatar)',
            'especialidade': 'Especialidade Profissional',
            'bio': 'Biografia Curta',
            'portfolio_url': 'Link de Portfólio / GitHub / Behance',
            'location': 'Localização',
            'available_for_hire': 'Disponível para novos projetos e contratações',
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=60, required=False, label="Nome Completo", widget=forms.TextInput(attrs={'class': 'form-control-art', 'placeholder': 'Seu Nome'}))
    email = forms.EmailField(required=True, label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control-art'}))

    class Meta:
        model = User
        fields = ('first_name', 'email')


class HiringRequestForm(forms.ModelForm):
    class Meta:
        model = HiringRequest
        fields = ('client_name', 'client_email', 'project_title', 'budget', 'message')
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Seu Nome Completo ou Empresa',
                'required': 'required'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'seuemail@exemplo.com',
                'required': 'required'
            }),
            'project_title': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Abertura 3D para YouTube / Loop VFX',
                'required': 'required'
            }),
            'budget': forms.TextInput(attrs={
                'class': 'form-control-art currency-mask-input',
                'placeholder': 'R$ 0,00',
                'autocomplete': 'off',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control-art',
                'rows': 4,
                'placeholder': 'Descreva os objetivos do projeto, prazos desejados, formato e referências visuais.',
                'required': 'required'
            }),
        }
        labels = {
            'client_name': 'Seu Nome / Empresa',
            'client_email': 'E-mail para Retorno',
            'project_title': 'Assunto / Nome do Projeto',
            'budget': 'Orçamento Estimado (Opcional)',
            'message': 'Mensagem e Detalhes da Proposta',
        }


class ProjectForm(forms.ModelForm):
    is_for_sale = forms.BooleanField(
        required=False,
        initial=False,
        label="Disponibilizar para venda / download de arquivos (Opcional)",
        widget=forms.CheckboxInput(attrs={'id': 'id_is_for_sale', 'class': 'custom-sale-checkbox'})
    )

    duration = forms.CharField(
        required=False,
        initial='0:30',
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Project
        fields = ('title', 'category', 'is_for_sale', 'price', 'duration', 'video_demo', 'description')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Animação Futurista Neon / Loop Cyberpunk',
                'required': 'required'
            }),
            'category': forms.Select(attrs={'class': 'form-control-art'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control-art',
                'id': 'id_project_price',
                'placeholder': '0.00 (Opcional - deixe vazio para exibição gratuita)',
                'step': '0.50'
            }),
            'video_demo': forms.FileInput(attrs={
                'class': 'avatar-file-input',
                'id': 'projectVideoInput',
                'accept': 'video/mp4,video/webm,video/ogg,video/quicktime,video/*,image/gif'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control-art',
                'rows': 3,
                'placeholder': 'Conte sobre as ferramentas usadas (Blender, After Effects, Cinema 4D, Houdini...), tempo de render e conceito.'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_for_sale = cleaned_data.get('is_for_sale')
        price = cleaned_data.get('price')
        if not is_for_sale:
            cleaned_data['price'] = 0.00
        elif not price or price <= 0:
            cleaned_data['price'] = 49.90
        return cleaned_data
        labels = {
            'title': 'Título do Projeto *',
            'category': 'Categoria de Motion *',
            'is_for_sale': 'Disponibilizar para Venda?',
            'price': 'Preço do Modelo / Asset (R$) (Opcional)',
            'duration': 'Duração da Animação',
            'thumbnail': 'Capa / Thumbnail (Opcional)',
            'video_demo': 'Arquivo de Vídeo Motion (MP4, WebM, MOV, GIF) *',
            'description': 'Descrição do Projeto',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].required = False
        self.fields['duration'].required = False
        self.fields['is_for_sale'].required = False

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if not price or price <= 0:
            return 0.00
        return price

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if not duration:
            return '0:30'
        return duration

    def clean(self):
        cleaned_data = super().clean()
        is_for_sale = cleaned_data.get('is_for_sale')
        price = cleaned_data.get('price')

        if not is_for_sale:
            cleaned_data['is_for_sale'] = False
            cleaned_data['price'] = 0.00
        else:
            if not price or price <= 0:
                cleaned_data['price'] = 29.90
        return cleaned_data



class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control-art comment-input',
                'rows': 2,
                'placeholder': 'Deixe um comentário sobre esta arte, feedback ou dúvidas sobre o modelo...',
                'required': 'required'
            })
        }
        labels = {
            'text': ''
        }


class PartnershipProposalForm(forms.ModelForm):
    class Meta:
        model = PartnershipProposal
        fields = ('title', 'roles', 'message')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Animação Curta Metragem / Co-criação de Clipe',
                'required': 'required'
            }),
            'roles': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Eu faço Modelagem 3D & Você faz Texturização e Animação'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control-art',
                'rows': 4,
                'placeholder': 'Descreva sua ideia de colaboração, referências visuais e como vocês podem somar técnicas.',
                'required': 'required'
            })
        }
        labels = {
            'title': 'Ideia / Nome do Projeto Conjunto',
            'roles': 'Divisão de Papéis / Habilidades',
            'message': 'Mensagem Inicial de Parceria'
        }


class PartnershipMessageForm(forms.ModelForm):
    class Meta:
        model = PartnershipMessage
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control-art chat-input-field',
                'placeholder': 'Escreva uma mensagem para o artista...',
                'required': 'required',
                'autocomplete': 'off'
            })
        }
        labels = {
            'text': ''
        }


class UserSuggestionForm(forms.ModelForm):
    class Meta:
        model = UserSuggestion
        fields = ('suggestion_type', 'title', 'message', 'name', 'email')
        widgets = {
            'suggestion_type': forms.Select(attrs={'class': 'form-control-art'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Adicionar filtro por tempo de render ou suporte a Blender 4.2',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control-art',
                'rows': 4,
                'placeholder': 'Conte para nós o que você gostaria de ver no ArtFlow, ideias de parcerias, ferramentas ou melhorias...',
                'required': 'required'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Seu Nome ou @user (Opcional)'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'seuemail@exemplo.com (Opcional)'
            }),
        }
        labels = {
            'suggestion_type': 'Categoria da Sugestão',
            'title': 'Título da Ideia / Sugestão *',
            'message': 'Descreva sua sugestão em detalhes *',
            'name': 'Seu Nome / Usuário',
            'email': 'Seu E-mail de Contato (Opcional)',
        }