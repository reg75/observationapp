from flask import render_template, request, redirect, url_for, make_response
from app.models import Observation, User
from app.forms import ObservationForm
from app.models import db
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from weasyprint import HTML
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
         return redirect(url_for('index'))
      
      except Exception as e:
         print(f"Error saving observation: {e}")
         db.session.rollback()
         raise e

   return render_template('new.html', new_observation_form=new_observation_form)


def register_routes(app):

   @app.route('/', methods=['GET'])
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
   def new_observation_route():
      # EN: Route for new_observation()
      # BR: Rota por new_observation() (nova nova observação de aula) 
        return new_observation()

   
   @app.route('/delete/<int:id>')
   def delete(id):
      # EN: Deletes observation by ID
      # BR: Apaga observação por ID
      observation_to_delete = Observation.query.get_or_404(id)

      try:
         db.session.delete(observation_to_delete)
         db.session.commit()
         return redirect('/')
      except:
         return 'There was a problem deleting that observation'

   
   @app.route('/view/observation/<int:observation_id>', methods=['GET'])
   def view_observation(observation_id):
      # EN: View a specific observation by ID
      # BR: Visualiza específica observação por ID
      observation = Observation.query.get_or_404(observation_id)

      return render_template('observation.html', observation=observation)

   @app.route('/download/<int:observation_id>', methods=['GET'])
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
