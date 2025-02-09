import WithId
import Plan
import Transactions
import Gateways

class Customer(WithId):
    def __init__(self, email, password, document_type, document_number):
        #super().__init__(self.create_id(email, password));
        self.email = email
        self.password = password
        self.document_type = document_type
        self.document_number = document_number

    def get_email(self):
        return self.email

    def get_document_type(self):
        return self.document_type

    def get_document_number(self):
        return self.document_number
"""
package gestorAplicacion.customers;

import gestorAplicacion.WithId;

public class Customer extends WithId {
    protected String email;
    protected String password;
    protected DocumentType documentType;
    protected String documentNumber;

    public Customer(
        String email,
        String password,
        DocumentType documentType,
        String documentNumber
    ) {
        super(createId(email, password));
        this.email = email;
        this.password = password;
        this.documentType = documentType;
        this.documentNumber = documentNumber;
    }

    public String getEmail() {
        return email;
    }

    public DocumentType getDocumentType() {
        return documentType;
    }

    public String getDocumentNumber() {
        return documentNumber;
    }
}
"""
class Admin(Customer):
    def __init__(self, email, password, document_type, document_number):
        super(email, password, document_type, document_number)

    def create_plan(self, name, description, price):
        #plan = Plan(name, description, price)
        #Repository.save(plan)
        return plan

    def configure_gateway(self, gateway, public_key, private_key):
        #credential = Credential(public_key, private_key, gateway)
        #Repository.save(credential)
        return credential

    def inactivate(self, plan):
        #Repository.update(plan)
"""
package gestorAplicacion.customers;

import java.io.File;

import baseDatos.Repository;
import gestorAplicacion.gateways.Credential;
import gestorAplicacion.gateways.Gateway;
import gestorAplicacion.plan.Plan;

public class Admin extends Customer {

    public Admin(
        String email,
        String password,
        DocumentType documentType,
        String documentNumber
    ) {
        super(email, password, documentType, documentNumber);
    }

    public Plan createPlan(String name, String description, double price) {
        Plan plan = new Plan(name, description, price);
        Repository.save(plan);
        return plan;
    }

    public Credential configureGateway(Gateway gateway, String publicKey, String privateKey) {
        Credential credential = new Credential(publicKey, privateKey, gateway);
        Repository.save(credential);
        return credential;
    }

    public void inactivate(Plan plan) {
        Repository.update(plan);
    }
}
"""
class User(Customer):
    def __init__(self, email, password, document_type, document_number):
        super().__init__(email, password, document_type, document_number)
    
    def change_subscription_payment_method(self, subscription, card):
        #subscription.set_payment_method(card)
        """
        transaction = Transaction(
            subscription.get_plan().get_name(),
            subscription.get_user(),
            1,
            TransactionStatus.PENDING
        )
        """
        #subscription.process_payment(transaction)
        return transaction.get_status() == TransactionStatus.ACCEPTED
    
    def save_on_repository_and_add_to_subscriptions(self, subscription):
        #Repository.save(subscription, "Subscription" + File.separator + subscription.get_plan().get_name())
        if self.subscriptions != None:
            self.subscriptions.append(subscription)
        else:
            self.subscriptions = []
            self.subscriptions.append(subscription)

    def add_subscription(self, plan):
        #subscription = Subscription(self, plan)
        #initial_charge_transaction = None
        if self.has_credit_card():
            #initial_charge_transaction = subscription.process_payment()
        self.save_on_repository_and_add_to_subscriptions(subscription)
        return initial_charge_transaction
    
    def add_subscription(self, plan, card):
        #subscription = Subscription(self, plan, card)
        #initial_charge_transaction = subscription.process_payment()
        self.save_on_repository_and_add_to_subscriptions(subscription)
        return initial_charge_transaction
    
    def get_user_subscribed_plans(self):
        user_subscriptions = self.get_subscriptions()
        plans = []
        for subscription in user_subscriptions:
            #plans.append(subscription.get_plan())
        return plans
    
    def get_subscriptions(self):
        #plans = Plan.get_all()
        user_subscriptions = []
        for plan in plans:
            """
            id = WithId.create_id(self.email, plan.get_name())
            subscription = Repository.load("Subscription" + File.separator + plan.get_name(), id)
            if subscription != None:
                subscription.set_user(self)
                subscription.set_plan(plan)
                if subscription.get_next_charge_date().is_before(LocalDate.now()):
                    subscription.set_status(SubscriptionStatus.CANCELLED)
                    subscription.set_suspension_date(subscription.get_next_charge_date())
                    subscription.set_next_charge_date(LocalDate.MIN)
                    Repository.update(subscription, "Subscription" + File.separator + plan.get_name())
                user_subscriptions.append(subscription)
            """
        self.subscriptions = user_subscriptions
        return user_subscriptions
    
    def get_inactive_subscriptions(self):
        #inactive_plans = Plan.get_inactive_plans()
        inactive_subscriptions = []
        for plan in inactive_plans:
            """
            id = WithId.create_id(self.email, plan.get_name())
            subscription = Repository.load("Subscription" + File.separator + plan.get_name(), id)
            if subscription != None:
                subscription.set_user(self)
                subscription.set_plan(plan)
                inactive_subscriptions.append(subscription)
            """
        return inactive_subscriptions
    
    def has_credit_card(self):
        #return len(Repository.load_all_object_in_directory(self.document_number)) > 0

    def add_credit_card(self, card):
        #Repository.save(card, "Card" + File.separator + self.get_id())
        return True
    
    def remove_credit_card(self, card):
        #Repository.delete(card, "Card" + File.separator + self.get_id())

    def get_credit_cards(self):
        #cards = Repository.load_all_object_in_directory("Card" + File.separator + self.get_id())
        user_cards = []
        for card in cards:
            user_cards.append(card)
        return user_cards
    
    def get_gateway(self):
        return self.gateway
"""
package gestorAplicacion.customers;

import java.io.File;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import baseDatos.Repository;
import gestorAplicacion.WithId;
import gestorAplicacion.gateways.Gateway;
import gestorAplicacion.plan.Plan;
import gestorAplicacion.plan.Subscription;
import gestorAplicacion.plan.SubscriptionStatus;
import gestorAplicacion.transactions.Card;
import gestorAplicacion.transactions.Transaction;
import gestorAplicacion.transactions.TransactionStatus;

public class User extends Customer {
    private Gateway gateway;
    private static final long serialVersionUID = 1L;
    // use transient to avoid serialization of this field
    // subscriptions are loaded from disk when needed
    private transient List<Subscription> subscriptions;

    public User(String email, String password, DocumentType documentType, String documentId, Gateway gateway) {
        super(email, password, documentType, documentId);
        this.gateway = gateway;
    }

    public boolean changeSubscriptionPaymentMethod(Subscription subscription, Card card) {
        if (subscription == null) {
            return false;
        }
        subscription.setPaymentMethod(card);

        Transaction transaction = new Transaction(
            subscription.getPlan().getName(),
            subscription.getUser(),
            1,
            TransactionStatus.PENDING
        );
        subscription.processPayment(transaction);
        return transaction.getStatus() == TransactionStatus.ACCEPTED;
    }

    private void saveOnRepositoryAndAddToSubscriptions(Subscription subscription) {
        Repository.save(subscription, "Subscription" + File.separator + subscription.getPlan().getName());
        if (this.subscriptions != null) {
            subscriptions.add(subscription);
        } else {
            this.subscriptions = new ArrayList<>();
            this.subscriptions.add(subscription);
        }
    }

    public Transaction addSubscription(Plan plan) {
        Subscription subscription = new Subscription(this, plan);
        Transaction initialChargeTransaction = null;
       if (hasCreditCard()) {
            initialChargeTransaction = subscription.processPayment();
        }
        saveOnRepositoryAndAddToSubscriptions(subscription);
       return initialChargeTransaction;
    }

    public Transaction addSubscription(Plan plan, Card card) {
        Subscription subscription = new Subscription(this, plan, card);
        Transaction initialChargeTransaction = subscription.processPayment();
        saveOnRepositoryAndAddToSubscriptions(subscription);
       return initialChargeTransaction;
    }

    public List<Plan> getUserSubscribedPlans() {
        ArrayList<Subscription> useSubscriptions = (ArrayList<Subscription>) getSubscriptions();
        ArrayList<Plan> plans = new ArrayList<>();
        for (Subscription subscription : useSubscriptions) {
            plans.add(subscription.getPlan());
        }
        return plans;
    }

    public List<Subscription> getSubscriptions() {
        List<Plan> plans = Plan.getAll();
        ArrayList<Subscription> userSubscriptions = new ArrayList<>();
        for (Plan plan : plans) {
            String id = WithId.createId(this.email, plan.getName());
            Subscription subscription = (Subscription) Repository.load(
                "Subscription" + File.separator + plan.getName(),
                id
            );
            if (subscription != null) {
                subscription.setUser(this);
                subscription.setPlan(plan);
                if(subscription.getNextChargeDate().isBefore(LocalDate.now())) {
                    subscription.setStatus(SubscriptionStatus.CANCELLED);
                    subscription.setSuspensionDate(subscription.getNextChargeDate());
                    subscription.setNextChargeDate(LocalDate.MIN);
                    Repository.update(subscription, "Subscription" + File.separator + plan.getName());
                }
                userSubscriptions.add(subscription);
            }
        }
        this.subscriptions = userSubscriptions;

        return userSubscriptions;
    }

    public List<Subscription> getInactiveSubscriptions() {
        List<Plan> inactivePlans = Plan.getInactivePlans();
        List<Subscription> inactiveSubscriptions = new ArrayList<>();
        for (Plan plan : inactivePlans) {
            String id = WithId.createId(this.email, plan.getName());
            Subscription subscription = (Subscription) Repository.load(
                "Subscription" + File.separator + plan.getName(),
                id
            );
            if (subscription != null) {
                subscription.setUser(this);
                subscription.setPlan(plan);
                inactiveSubscriptions.add(subscription);
            }
        }
        return inactiveSubscriptions;
    }

    public boolean hasCreditCard() {
        return !Repository.loadAllObjectInDirectory(documentNumber).isEmpty();
    }

    public boolean addCreditCard(Card card) {
        Repository.save(card, "Card" + File.separator + this.getId());
        return true;
    }

    public void removeCreditCard(Card card) {
        Repository.delete(card, "Card" + File.separator + this.getId());
    }

    public List<Card> getCreditCards() {
        List<WithId> cards = Repository.loadAllObjectInDirectory("Card" + File.separator + this.getId());
        List<Card> userCards = new ArrayList<>();
        for (WithId card : cards) {
            userCards.add((Card) card);
        }
        return userCards;
    }

    public Gateway getGateway() {
        return this.gateway;
    }


}
"""
class DocumentType(Enum):
    CC = "CC"
    CE = "CE"
    TI = "TI"
    PP = "PP"
    NIT = "NIT"
"""
package gestorAplicacion.customers;

public enum DocumentType {
    CC, CE, TI, PP, NIT
}
"""