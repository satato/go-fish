//imports math for use with math functions and Math.random() throughout the program
import java.math.*;
import java.util.ArrayList;
import java.util.Random;

//sets up the main class
public class main {
	//defines global variables for use throughout the class
	//defines the 'cards' array containing all possible card identities in a deck of cards
	static String[] cards = {"Ace-H","2-H","3-H","4-H","5-H","6-H","7-H","8-H","9-H","10-H","Jack-H","Queen-H","King-H","Ace-S","2-S","3-S","4-S","5-S","6-S","7-S","8-S","9-S","10-S","Jack-S","Queen-S","King-S","Ace-D","2-D","3-D","4-D","5-D","6-D","7-D","8-D","9-D","10-D","Jack-D","Queen-D","King-D","Ace-C","2-C","3-C","4-C","5-C","6-C","7-C","8-C","9-C","10-C","Jack-C","Queen-C","King-C"};
	//prepares the user's hand and the computer's hand to be given cards
	static ArrayList<String> hpHand = new ArrayList<String>();
	static ArrayList<String> cpHand = new ArrayList<String>();
	//initially creates the deck of cards to be drawn from
	static ArrayList<String> deck = new ArrayList<String>();
	//sets up a random object for use with determining stuff ~randomly~
	static Random rand = new Random();
	//sets up an arraylist containing all of HP's past guesses
	static ArrayList<String> guesses = new ArrayList<String>();
	//creates arraylists containing each players' gathered sets of cards
	static ArrayList<String> hpSets = new ArrayList<String>();
	static ArrayList<String> cpSets = new ArrayList<String>();

	//sets up the 'main'; aka what first runs when the program is run
	public static void main(String[] args) {

		//fills the arraylist 'deck' with all the cards from the 'cards' array
		fillDeck();

		//gives each player their 7 starting cards and removes them from the deck/draw pile
		for(int i=0; i<7; i++) {

			//randomly selects a card from the deck
			int workingIndex = rand.nextInt(deck.size());
			String currentCard = deck.get(workingIndex);
			//gives the human player the randomly selected card and removes it from the deck
			hpHand.add("currentCard");
			deck.remove(workingIndex);
			//randomly selects a card from the deck
			workingIndex = rand.nextInt(deck.size());
			currentCard = deck.get(workingIndex);
			//gives the computer player the randomly selected card and removes it from the deck
			cpHand.add(currentCard);
			deck.remove(workingIndex);
		}

	}

	//fills the arraylist 'deck' with all the cards from the 'cards' array
	public static void fillDeck() {
		for(int a = 0; a<cards.length; a++) {
			deck.add(cards[a]);
		}
	}

	public static void gameStart() {

	}

	public static void compNewHand() {

	}

	public static void userNewHand() {

	}

	public static void userDraw() {

		if(deck.size()>0) {
			//randomly selects a card from the deck
			int workingIndex = rand.nextInt(deck.size());
			String currentCard = deck.get(workingIndex);
			//gives the human player the randomly selected card and removes it from the deck
			hpHand.add("currentCard");
			deck.remove(workingIndex);
		}
		else {
			gameEnd();
		}

	}

	public static void compDraw() {
		//randomly selects a card from the deck
		int workingIndex = rand.nextInt(deck.size());
		String currentCard = deck.get(workingIndex);
		//gives the computer player the randomly selected card and removes it from the deck
		cpHand.add("currentCard");
		deck.remove(workingIndex);
	}

	public static void humanTurn() {
		System.out.println("\n-------------------------------------------------\nYour Turn\n");
		System.out.println("Opponent's Sets:");
		if(cpSets.size()==0)
			System.out.print("none");
		else {
			for(int b = 0; b<cpSets.size(); b++) {
				System.out.println(cpSets.get(b));
			}
		}

		System.out.println("\nYour Sets:");
		if(hpSets.size()==0)
			System.out.print("none");
		else {
			for(int c = 0; c<hpSets.size(); c++) {
				System.out.println(hpSets.get(c));
			}

		System.out.println("\nYour Cards:");
		if(hpHand.size()==0)
			userDraw();
		else {
			for(int d = 0; d<hpHand.size(); d++) {
				System.out.println(hpHand.get(d));
			}
		}

		}

	}

	public static void gameEnd() {

	}
}
