document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('bookingForm');
  const checkIn = document.getElementById('checkIn');
  const checkOut = document.getElementById('checkOut');
  const roomType = document.getElementById('roomType');
  const breakfast = document.getElementById('breakfast');
  const transfer = document.getElementById('transfer');
  const totalPriceEl = document.getElementById('totalPrice');
  const modal = document.getElementById('resultModal');
  const modalDetails = document.getElementById('modalDetails');
  const closeModalBtn = document.getElementById('closeModalBtn');

  // Установка дат по умолчанию (сегодня и завтра)
  const today = new Date();
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  checkIn.value = today.toISOString().split('T')[0];
  checkOut.value = tomorrow.toISOString().split('T')[0];

  function calculatePrice() {
    const d1 = new Date(checkIn.value);
    const d2 = new Date(checkOut.value);
    const timeDiff = d2 - d1;
    const nights = Math.max(1, Math.round(timeDiff / (1000 * 3600 * 24)));
    
    const selectedOption = roomType.options[roomType.selectedIndex];
    const roomRate = parseInt(selectedOption.getAttribute('data-price') || '3500');
    
    let total = roomRate * nights;
    if (breakfast.checked) total += 800 * nights;
    if (transfer.checked) total += 1500;
    
    totalPriceEl.textContent = total.toLocaleString('ru-RU') + ' ₽';
    return { nights, total };
  }

  [checkIn, checkOut, roomType, breakfast, transfer].forEach(el => {
    el.addEventListener('change', calculatePrice);
  });
  calculatePrice();

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const fullName = document.getElementById('fullName').value.trim();
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();
    
    let isValid = true;
    if (fullName.length < 3) {
      document.getElementById('nameError').textContent = 'Укажите полное имя (мин. 3 символа)';
      isValid = false;
    } else {
      document.getElementById('nameError').textContent = '';
    }

    if (!email.includes('@') || !email.includes('.')) {
      document.getElementById('emailError').textContent = 'Введите корректный email';
      isValid = false;
    } else {
      document.getElementById('emailError').textContent = '';
    }

    if (phone.length < 7) {
      document.getElementById('phoneError').textContent = 'Введите номер телефона';
      isValid = false;
    } else {
      document.getElementById('phoneError').textContent = '';
    }

    if (!isValid) return;

    const { nights, total } = calculatePrice();
    modalDetails.textContent = `Гость: ${fullName}\nНомер: ${roomType.options[roomType.selectedIndex].text}\nСрок: ${nights} ноч.\nСумма: ${total.toLocaleString('ru-RU')} ₽`;
    modal.classList.remove('hidden');
  });

  closeModalBtn.addEventListener('click', () => {
    modal.classList.add('hidden');
    form.reset();
    calculatePrice();
  });
});