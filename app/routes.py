from flask import render_template, request, redirect, url_for, make_response, flash
from app.models import Observation, User
from app.forms import ObservationForm
from app.models import db
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from weasyprint import HTML
from flasgger import swag_from
import datetime


def new_observation():
   # EN: Creates new observation
   # BR: Cria nova observação de aula
   
   new_observation_form = ObservationForm()
   teachers = User.query.order_by(User.User_Surname).all()
   teacher_choices = [(teacher.User_ID, f'{teacher.User_Forename} {teacher.User_Surname}') for teacher in teachers]
   new_observation_form.Observation_Teacher.choices = teacher_choices
   
   if request.method == 'POST' and new_observation_form.validate_on_submit():

      
      try:
         new_observation = Observation(
            Observation_Date=datetime.datetime.now(),
            Observation_Teacher=new_observation_form.Observation_Teacher.data,
            Observation_Class=new_observation_form.Observation_Class.data,
            Observation_Focus=new_observation_form.Observation_Focus.data,
            Observation_Strengths=new_observation_form.Observation_Strengths.data,
            Observation_Weaknesses=new_observation_form.Observation_Weaknesses.data,
            Observation_Comments=new_observation_form.Observation_Comments.data,
)


         
         db.session.add(new_observation)
         db.session.commit()
         flash("Observation added!", "success")
         return redirect(url_for('index'))
      
      except Exception as e:
         print(f"Error saving observation: {e}")
         db.session.rollback()
         raise e

   return render_template('new.html', new_observation_form=new_observation_form)


def register_routes(app):

   @app.route('/', methods=['GET'])
   @swag_from({
      'tags': ['Observations / Observações'],
      'summary': 'View all observations / Visualizar todas as observações',
      'description': (
         'Displays the list of previous observations in descending order of date. / '
         'Exibe a lista de observações anteriores em ordem decrescente de data.'
      ),
      'responses': {
         200: {
               'description': 'List of observations retrieved successfully. / '
                              'Lista de observações recuperada com sucesso.'
         }
      }
   })
   def index():
      # EN: Home page - returns list of previous observations
      # BR: Página inicial - retorna lista de observações
      observations = (
    Observation.query.options(joinedload(Observation.Teacher))
    .order_by(desc(Observation.Observation_Date))
    .all()
)
      return render_template('index.html', observations=observations)

   @app.route('/view/new', methods=['GET', 'POST'])
   @swag_from({
      'tags': ['Observations / Observações'],
      'summary': 'Create a new observation / Criar uma nova observação',
      'description': (
         'Displays a form to create a new observation. Saves the observation data on submission. / '
         'Exibe um formulário para criar uma nova observação. Salva os dados da observação ao enviar.'
      ),
      'parameters': [
         {
            'name': 'ObservationForm',
            'in': 'body',
            'required': True,
            'schema': {
               'type': 'object',
               'properties': {
                  'Observation_Teacher': {
                     'type': 'integer',
                     'description': (
                        'ID of the teacher. Must match an existing ID in the database (e.g., User table). / '
                        'ID do professor. Deve corresponder a um ID existente no banco de dados (por exemplo, tabela User).'
                     ),
                     'enum': [1, 2, 3, 4]
                  },
                  'Observation_Class': {
                     'type': 'string',
                     'description': 'Class observed / Aula observada'
                  },
                  'Observation_Focus': {
                     'type': 'string',
                     'description': 'Focus of the observation / Foco da observação'
                  },
                  'Observation_Strengths': {
                     'type': 'string',
                     'description': 'Strengths observed / Pontos fortes observados'
                  },
                  'Observation_Weaknesses': {
                     'type': 'string',
                     'description': 'Weaknesses observed / Pontos fracos observados'
                  },
                  'Observation_Comments': {
                     'type': 'string',
                     'description': 'Additional comments / Comentários adicionais'
                  }
               },
               'required': ['Observation_Teacher', 'Observation_Class', 'Observation_Focus']
            }
         }
      ],
      'responses': {
         200: {
            'description': 'Observation form displayed successfully. / '
                           'Formulário de observação exibido com sucesso.'
         },
         302: {
            'description': 'Observation created and redirected to home. / '
                           'Observação criada e redirecionada para a página inicial.'
         },
         500: {
            'description': 'Error creating the observation. / Erro ao criar a observação.'
         }
      }
   })
   def new_observation_route():
      # EN: Route for new_observation()
      # BR: Rota por new_observation() (nova nova observação de aula) 
        return new_observation()

   
   @app.route('/delete/<int:id>')
   @app.route('/delete/<int:id>', methods=['DELETE'])
   @swag_from({
      'tags': ['Observations / Observações'],
      'summary': 'Delete an observation by ID / Apagar uma observação por ID',
      'description': (
         'Deletes an observation from the database based on its unique ID. / '
         'Apaga uma observação do banco de dados com base no seu ID único.'
      ),
      'parameters': [
         {
            'name': 'id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': (
               'The unique ID of the observation to delete. Must exist in the database. / '
               'O ID único da observação a ser apagada. Deve existir no banco de dados.'
            ),
            'example': 5
         }
      ],
      'responses': {
         200: {
            'description': 'Observation deleted successfully. / '
                           'Observação apagada com sucesso.'
         },
         404: {
            'description': 'Observation not found. / Observação não encontrada.'
         },
         500: {
            'description': 'Error deleting the observation. / Erro ao apagar a observação.'
         }
      }
   })
   def delete(id):
      # EN: Deletes observation by ID
      # BR: Apaga observação por ID
      observation_to_delete = Observation.query.get_or_404(id)

      try:
         db.session.delete(observation_to_delete)
         db.session.commit()
         flash("Observation deleted!", "success")
         return redirect('/')
      except:
         return 'There was a problem deleting that observation'

   
   @app.route('/view/observation/<int:observation_id>', methods=['GET'])
   @swag_from({
      'tags': ['Observations / Observações'],
      'summary': 'View a specific observation by ID / Visualizar uma observação específica por ID',
      'description': (
         'Fetches and displays the details of a specific observation based on its unique ID. / '
         'Recupera e exibe os detalhes de uma observação específica com base no seu ID único.'
      ),
      'parameters': [
         {
            'name': 'observation_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': (
               'The unique ID of the observation to view. Must exist in the database. / '
               'O ID único da observação a ser visualizada. Deve existir no banco de dados.'
            ),
            'example': 3
         }
      ],
      'responses': {
         200: {
            'description': 'Observation details retrieved successfully. / '
                           'Detalhes da observação recuperados com sucesso.',
            'content': {
               'text/html': {
                  'example': 'Rendered HTML page with observation details. / Página HTML renderizada com detalhes da observação.'
               }
            }
         },
         404: {
            'description': 'Observation not found. / Observação não encontrada.'
         },
         500: {
            'description': 'Error retrieving the observation. / Erro ao recuperar a observação.'
         }
      }
   })
   def view_observation(observation_id):
      # EN: View a specific observation by ID
      # BR: Visualiza específica observação por ID
      observation = Observation.query.get_or_404(observation_id)

      return render_template('observation.html', observation=observation)

   @app.route('/download/<int:observation_id>', methods=['GET'])
   @swag_from({
      'tags': ['Observations / Observações'],
      'summary': 'Download observation as PDF / Baixar observação como PDF',
      'description': (
         
         'Generates a PDF containing the details of a specific observation identified by its unique ID. / '
         'Gera um PDF contendo os detalhes de uma observação específica identificada pelo seu ID único.'
      ),
      'parameters': [
         {
            'name': 'observation_id',
            'in': 'path',
            'required': True,
            'type': 'integer',
            'description': (
               'The unique ID of the observation to download as PDF. Must exist in the database. / '
               'O ID único da observação a ser baixada como PDF. Deve existir no banco de dados.'
            ),
            'example': 3
         }
      ],
      'responses': {
         200: {
            'description': 'PDF generated and returned successfully. / '
                           'PDF gerado e retornado com sucesso.',
            'content': {
               'application/pdf': {
                  'example': 'Binary PDF data stream. / Fluxo de dados binários do PDF.'
               }
            }
         },
         404: {
            'description': 'Observation not found. / Observação não encontrada.'
         },
         500: {
            'description': 'Error generating the PDF. / Erro ao gerar o PDF.'
         }
      }
   })
   def download_pdf(observation_id):
      # EN: Saves observation in pdf format
      # BR: Salva observação como pdf
      try:
         observation = Observation.query.get_or_404(observation_id)

         rendered_html = render_template('pdf_form.html', observation=observation)

         pdf = HTML(string=rendered_html).write_pdf()

         response = make_response(pdf)
         response.headers['Content-Type'] = 'application/pdf'
         response.headers['Content-Disposition'] = f'attachment; filename=observation_{observation.Observation_Date.strftime("%Y-%m-%d")}.pdf'

         return response

      except Exception as e:
         print(f"Error in download_pdf: {e}")
         return "An error occurred while generating the PDF", 500
