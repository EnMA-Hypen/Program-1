import random

class Card:
    """Kelas untuk merepresentasikan satu kartu"""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank} of {self.suit}"
    
    def get_value(self):
        """Mengembalikan nilai kartu"""
        if self.rank in ['King', 'Queen', 'Jack']:
            return 10
        elif self.rank == 'Ace':
            return 11
        else:
            return int(self.rank)


class Deck:
    """Kelas untuk merepresentasikan dek kartu"""
    def __init__(self):
        self.cards = []
        self.initialize_deck()
    
    def initialize_deck(self):
        """Inisialisasi dek dengan 52 kartu"""
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
    
    def shuffle(self):
        """Mengacak dek"""
        random.shuffle(self.cards)
    
    def draw_card(self):
        """Mengambil satu kartu dari dek"""
        if len(self.cards) == 0:
            self.initialize_deck()
            self.shuffle()
        return self.cards.pop()
    
    def draw_card_limited(self):
        """Mengambil kartu dengan nilai 1-6 (Ace, 2, 3, 4, 5, 6) untuk dealer"""
        # Filter kartu dengan nilai 1-6
        limited_cards = [card for card in self.cards if card.get_value() in [1, 2, 3, 4, 5, 6]]
        
        if len(limited_cards) == 0:
            # Jika tidak ada kartu dengan nilai 1-6, initialize ulang dek
            self.initialize_deck()
            self.shuffle()
            limited_cards = [card for card in self.cards if card.get_value() in [1, 2, 3, 4, 5, 6]]
        
        # Ambil kartu acak dari kartu yang terbatas
        selected_card = random.choice(limited_cards)
        self.cards.remove(selected_card)
        return selected_card


class Hand:
    """Kelas untuk merepresentasikan tangan pemain"""
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        """Menambah kartu ke tangan"""
        self.cards.append(card)
    
    def get_value(self):
        """Menghitung nilai total kartu dengan mempertimbangkan Ace"""
        total = 0
        aces = 0
        
        # Hitung nilai total kartu
        for card in self.cards:
            total += card.get_value()
            if card.rank == 'Ace':
                aces += 1
        
        # Jika nilai lebih dari 21 dan ada Ace bernilai 11, ubah menjadi 1
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        
        return total
    
    def display_cards(self, hide_first=False):
        """Menampilkan kartu yang dipegang"""
        if hide_first and len(self.cards) > 0:
            print(f"[Kartu Tersembunyi]")
            for card in self.cards[1:]:
                print(f"  {card}")
        else:
            for card in self.cards:
                print(f"  {card}")
    
    def get_cards_str(self, hide_first=False):
        """Mengembalikan string dari kartu yang dipegang"""
        cards_str = []
        if hide_first and len(self.cards) > 0:
            cards_str.append("[Kartu Tersembunyi]")
            for card in self.cards[1:]:
                cards_str.append(str(card))
        else:
            for card in self.cards:
                cards_str.append(str(card))
        return ", ".join(cards_str)


class BlackJack:
    """Kelas utama untuk game Black Jack"""
    def __init__(self, wortel):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.game_over = False
        self.player_stand = False
        self.wortel = wortel
        self.bet = 0
    
    def place_bet(self):
        """Menghandle penempatan taruhan"""
        print("\n" + "="*60)
        print("PENEMPATAN TARUHAN")
        print("="*60)
        print(f"\nWortel Anda saat ini: 🥕 {self.wortel}")
        print("\nMasukkan jumlah taruhan Anda (dalam satuan wortel 🥕)")
        
        while True:
            try:
                bet_input = input(f"\nMasukkan jumlah taruhan (1-{self.wortel}): ").strip()
                self.bet = int(bet_input)
                
                # Validasi input
                if self.bet <= 0:
                    print("❌ Taruhan harus lebih dari 0!")
                    continue
                
                if self.bet > self.wortel:
                    print(f"❌ Wortel Anda tidak cukup! Anda hanya memiliki 🥕 {self.wortel}.")
                    continue
                
                # Taruhan valid, kurangkan dari wortel
                self.wortel -= self.bet
                print(f"\n✓ Anda telah menambahkan taruhan sebesar 🥕 {self.bet}")
                print(f"Wortel tersisa: 🥕 {self.wortel}")
                break
                
            except ValueError:
                print("❌ Input tidak valid. Silakan masukkan angka bulat.")
    
    def deal_initial_cards(self):
        """Membagikan kartu awal (2 kartu untuk masing-masing)"""
        print("\n" + "="*60)
        print("PERMAINAN BLACK JACK DIMULAI!")
        print(f"Taruhan saat ini: 🥕 {self.bet}")
        print("="*60)
        
        # Bagikan kartu untuk pemain sampai dealer mendapat nilai 10-13
        dealer_value = 0
        
        # Loop sampai dealer mendapat nilai 10-13
        while dealer_value < 10 or dealer_value > 131:
            self.player_hand = Hand()
            self.dealer_hand = Hand()
            
            # Bagikan 2 kartu untuk pemain dan dealer
            for _ in range(2):
                self.player_hand.add_card(self.deck.draw_card())
                self.dealer_hand.add_card(self.deck.draw_card())
            
            dealer_value = self.dealer_hand.get_value()
            
            # Jika dealer tidak mendapat 10-13, ulangi
            if dealer_value < 10 or dealer_value > 13:
                print(f"⚠️  Dealer mendapat nilai {dealer_value}. Mengambil ulang kartu...")
        
        print(f"✓ Dealer mendapat nilai awal: {dealer_value}")
        self.display_game_state(hide_dealer=True)
    
    def display_game_state(self, hide_dealer=False):
        """Menampilkan status permainan"""
        print("\n" + "-"*60)
        print(f"Wortel Anda: 🥕 {self.wortel} | Taruhan: 🥕 {self.bet}")
        print("-"*60)
        print("TANGAN PEMAIN:")
        self.player_hand.display_cards()
        print(f"Total Nilai: {self.player_hand.get_value()}")
        
        print("\nTANGAN DEALER:")
        if hide_dealer:
            self.dealer_hand.display_cards(hide_first=True)
            print(f"Total Nilai: [Tersembunyi]")
        else:
            self.dealer_hand.display_cards()
            print(f"Total Nilai: {self.dealer_hand.get_value()}")
        print("-"*60)
    
    def player_turn(self):
        """Menghandle giliran pemain"""
        while not self.player_stand and not self.game_over:
            print("\nPILIHAN ANDA:")
            print("(d) Draw - Ambil kartu")
            print("(s) Stand - Selesaikan giliran")
            
            choice = input("\nMasukkan pilihan (d/s): ").lower().strip()
            
            if choice == 'd':
                print("\nPemain mengambil kartu...")
                self.player_hand.add_card(self.deck.draw_card())
                self.display_game_state(hide_dealer=True)
                
                if self.player_hand.get_value() > 21:
                    print("\n⚠️  BUST! Nilai pemain melebihi 21!")
                    self.game_over = True
                    return
                
            elif choice == 's':
                print("\nPemain STAND. Giliran pemain selesai!")
                self.player_stand = True
            else:
                print("Pilihan tidak valid. Silakan masukkan 'd' atau 's'.")
    
    def dealer_turn(self):
        """Menghandle giliran dealer secara otomatis"""
        print("\n" + "="*60)
        print("GILIRAN DEALER")
        print("="*60)
        
        while self.dealer_hand.get_value() < 17:
            print(f"\nDealer mengambil kartu...")
            # Dealer hanya bisa mengambil kartu dengan nilai 1-6
            self.dealer_hand.add_card(self.deck.draw_card_limited())
        
        if self.dealer_hand.get_value() > 21:
            print("\n⚠️  DEALER BUST! Nilai dealer melebihi 21!")
        else:
            print(f"\nDealer STAND")
    
    def determine_winner(self):
        """Menentukan pemenang"""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        
        print("\n" + "="*60)
        print("HASIL AKHIR")
        print("="*60)
        self.display_game_state(hide_dealer=False)
        
        winner = None
        
        # Jika pemain bust
        if player_value > 21:
            print("\n❌ PEMAIN BUST! Pemain melebihi 21.")
            print("🎉 DEALER MENANG!")
            print(f"\n💔 Anda kehilangan 🥕 {self.bet}")
            winner = "dealer"
        
        # Jika dealer bust
        elif dealer_value > 21:
            print("\n❌ DEALER BUST! Dealer melebihi 21.")
            print("🎉 PEMAIN MENANG!")
            winnings = self.bet * 2
            self.wortel += winnings
            print(f"\n🎉 Anda memenangkan 🥕 {winnings}!")
            winner = "player"
        
        # Jika kedua-duanya 21 (Natural Black Jack)
        elif player_value == 21 and dealer_value == 21:
            print("\n🤝 DRAW! Kedua pemain mendapat 21 (Black Jack)!")
            self.wortel += self.bet  # Kembalikan taruhan
            print(f"\n🤝 Taruhan Anda dikembalikan 🥕 {self.bet}")
            winner = "draw"
        
        # Jika pemain 21 dan dealer tidak
        elif player_value == 21:
            print("\n🎉 PEMAIN MENANG! Pemain mendapat 21 (Black Jack)!")
            winnings = self.bet * 2
            self.wortel += winnings
            print(f"\n🎉 Anda memenangkan 🥕 {winnings}!")
            winner = "player"
        
        # Jika dealer 21 dan pemain tidak
        elif dealer_value == 21:
            print("\n🎉 DEALER MENANG! Dealer mendapat 21 (Black Jack)!")
            print(f"\n💔 Anda kehilangan 🥕 {self.bet}")
            winner = "dealer"
        
        # Bandingkan nilai kedua pemain
        elif player_value > dealer_value:
            print(f"\n🎉 PEMAIN MENANG! ({player_value} > {dealer_value})")
            winnings = self.bet * 2
            self.wortel += winnings
            print(f"\n🎉 Anda memenangkan 🥕 {winnings}!")
            winner = "player"
        elif dealer_value > player_value:
            print(f"\n🎉 DEALER MENANG! ({dealer_value} > {player_value})")
            print(f"\n💔 Anda kehilangan 🥕 {self.bet}")
            winner = "dealer"
        else:
            print(f"\n🤝 DRAW! Kedua pemain memiliki nilai yang sama ({player_value})!")
            self.wortel += self.bet  # Kembalikan taruhan
            print(f"\n🤝 Taruhan Anda dikembalikan 🥕 {self.bet}")
            winner = "draw"
        
        print(f"\nTotal Wortel Anda sekarang: 🥕 {self.wortel}")
        return winner
    
    def play(self):
        """Menjalankan permainan"""
        self.place_bet()
        self.deal_initial_cards()
        
        # Periksa apakah pemain langsung mendapat 21 (Black Jack)
        # Dealer sudah dijamin nilai 10-13 di awal
        if self.player_hand.get_value() == 21:
            print("\n⚡ PEMAIN LANGSUNG MENDAPAT 21 (BLACK JACK)!")
            self.game_over = True
        else:
            # Giliran pemain
            self.player_turn()
        
        # Jika pemain tidak bust, giliran dealer
        if not self.game_over:
            self.dealer_turn()
        
        # Tentukan pemenang
        winner = self.determine_winner()
        
        return winner


def main():
    """Fungsi utama untuk menjalankan game"""
    print("\n" + "🎰 "*20)
    print("SELAMAT DATANG DI PERMAINAN BLACK JACK")
    print("🎰 "*20)
    
    wortel = 50  # Jumlah wortel awal
    player_wins = 0
    dealer_wins = 0
    draws = 0
    
    while True:
        # Periksa apakah wortel pemain kurang dari 0
        if wortel < 0:
            print("\n" + "="*60)
            print("⚠️  PERMAINAN BERAKHIR!")
            print("="*60)
            print(f"Wortel Anda telah habis! ({wortel})")
            print("Permainan di-reset dengan 50 wortel dan skor 0.")
            print("="*60 + "\n")
            wortel = 50
            player_wins = 0
            dealer_wins = 0
            draws = 0
        
        # Periksa apakah pemain masih memiliki wortel untuk bertaruh
        if wortel <= 0:
            print("\n" + "="*60)
            print("❌ TIDAK ADA WORTEL UNTUK BERTARUH!")
            print("="*60)
            print("Permainan di-reset.")
            print("="*60 + "\n")
            wortel = 50
            player_wins = 0
            dealer_wins = 0
            draws = 0
            continue
        
        game = BlackJack(wortel)
        winner = game.play()
        
        # Update wortel dari hasil permainan
        wortel = game.wortel
        
        # Update statistik
        if winner == "player":
            player_wins += 1
        elif winner == "dealer":
            dealer_wins += 1
        else:
            draws += 1
        
        # Tanyakan apakah ingin bermain lagi
        print("\n" + "-"*60)
        print(f"STATISTIK: Pemain: {player_wins} | Dealer: {dealer_wins} | Draw: {draws}")
        print(f"Total Wortel: 🥕 {wortel}")
        print("-"*60)
        
        while True:
            again = input("\nApakah Anda ingin bermain lagi? (y/n): ").lower().strip()
            if again in ['y', 'n']:
                if again == 'n':
                    print("\n" + "="*60)
                    print("TERIMA KASIH TELAH BERMAIN BLACK JACK!")
                    print("="*60)
                    print(f"\nSTATISTIK AKHIR:")
                    print(f"  Pemain Menang: {player_wins}")
                    print(f"  Dealer Menang: {dealer_wins}")
                    print(f"  Draw: {draws}")
                    print(f"  Total Wortel: 🥕 {wortel}")
                    print("="*60 + "\n")
                    return
                break
            else:
                print("Pilihan tidak valid. Silakan masukkan 'y' atau 'n'.")


if __name__ == "__main__":
    main()
