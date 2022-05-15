from django.forms import ModelForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages


from medication.models import Medication
# Create your views here.


class AddMedicineForm(ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'dosage', 'dosage_unit', 'day', 'time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['dosage'].widget.attrs.update({'class': 'form-control'})
        self.fields['dosage_unit'].widget.attrs.update(
            {'class': 'form-control'})


def index(request):
    if request.user.is_authenticated:
        if(request.method == 'POST'):
            form = AddMedicineForm(request.POST)
            if form.is_valid():
                medicine = form.save(commit=False)
                medicine.user = request.user
                medicine.save()
                return redirect("index")
            else:
                messages.error(
                    request, "Wrong form input")
        else:
            user_medicine = Medication.objects.filter(user=request.user)
            return render(request, 'medication/index.html', {
                'add_medicine_form': AddMedicineForm,
                'medications': user_medicine
            })
    else:
        return redirect('landing')


def landing(request):

    return render(request, 'medication/landing.html', {

    })


def edit(request, medication_id):
    if(request.method == 'POST'):
        medication = Medication.objects.get(id=medication_id)
        form = AddMedicineForm(instance=medication, data=request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(
                request, "Wrong form input")
        return redirect('index')
    else:
        medication = Medication.objects.get(id=medication_id)
        form = AddMedicineForm(instance=medication)
        return render(request, 'medication/editMedication.html', {'add_medicine_form': form, 'id': medication.id})


def delete(request, medication_id):
    medication = Medication.objects.get(id=medication_id)
    if(medication.user == request.user):
        medication.delete()
    return redirect("index")
