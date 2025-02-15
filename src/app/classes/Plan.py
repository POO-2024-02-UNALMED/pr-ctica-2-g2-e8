import WithId
import Customer
import Transactions
import Gateways

class Plan(WithId):
    def __init__(self, name, description, price):
        super().__init__(name)
        self.name = name
        self.description = description
        self.price = price
        #self.status = PlanStatus.ACTIVE

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    @staticmethod
    def get_all():
        #withIdList = Repository.load_all_object_in_directory("Plan")
        planList = []
        for withId in withIdList:
            #if isinstance(withId, Plan) and withId.get_status() == PlanStatus.ACTIVE:
                planList.append(withId)
        return planList

    @staticmethod
    def get_inactive_plans():
        #withIdList = Repository.load_all_object_in_directory("Plan")
        planList = []
        for withId in withIdList:
            if isinstance(withId, Plan) and withId.get_status() == PlanStatus.INACTIVE:
                planList.append(withId)
        return planList

    @staticmethod
    def get_subscriptions(plan):
        #withIdList = Repository.load_all_object_in_directory("Subscription" + os.sep + plan.get_name())
        subscriptionList = []
        for withId in withIdList:
            #if isinstance(withId, Subscription):
                subscriptionList.append(withId)
        return subscriptionList

    @staticmethod
    def inactivate_subscriptions(plan):
        #withIdList = Repository.load_all_object_in_directory("Subscription" + os.sep + plan.get_name())
        subscriptionList = []
        for withId in withIdList:
            """
            if isinstance(withId, Subscription):
                withId.set_status(SubscriptionStatus.INACTIVE)
                withId.set_suspension_date(withId.get_next_charge_date())
                withId.set_next_charge_date(LocalDate.MIN)
                Repository.update(withId, "Subscription" + os.sep + plan.get_name())
                subscriptionList.append(withId)
            """
        return subscriptionList

    """
    @staticmethod
    def get_plan(name):
        return Repository.load("Plan", name)
    """

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return f"Plan: {self.name}, Description: {self.description}, Price: {self.price}, Status: {self.status}"

    def __repr__(self):
        return f"Plan: {self.name}, Description

"""
package gestorAplicacion.plan;

import java.io.File;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

import baseDatos.Repository;
import gestorAplicacion.WithId;


public class Plan extends WithId {
    private String name;
    private String description;
    private double price;
    private PlanStatus status;

    public Plan(String name, String description, double price) {
        super(name);
        this.name = name;
        this.description = description;
        this.price = price;
        this.status = PlanStatus.ACTIVE;
    }

    public Plan(String id, String name, String description, double price) {
        super(id);
        this.name = name;
        this.description = description;
        this.price = price;
        this.status = PlanStatus.ACTIVE;
    }

    public String getName() {
        return name;
    }

    public String getDescription() {
        return description;
    }

    public double getPrice() {
        return price;
    }

    public static List<Plan> getAll() {
        List<WithId> withIdList = Repository.loadAllObjectInDirectory("Plan");
        List<Plan> planList = new ArrayList<>();
        for (WithId withId : withIdList) {
            if (withId instanceof Plan plan && plan.getStatus() == PlanStatus.ACTIVE) {
                planList.add(plan);
            }
        }
        return planList;
    }

    public static List<Plan> getInactivePlans() {
        List<WithId> withIdList = Repository.loadAllObjectInDirectory("Plan");
        List<Plan> planList = new ArrayList<>();
        for (WithId withId : withIdList) {
            if (withId instanceof Plan plan && plan.getStatus() == PlanStatus.INACTIVE) {
                planList.add(plan);
            }
        }
        return planList;
    }

    public static List<Subscription> getSubscriptions(Plan plan) {
        List<WithId> withIdList = Repository.loadAllObjectInDirectory("Subscription" + File.separator + plan.getName());
        List<Subscription> subscriptionList = new ArrayList<>();
        for (WithId withId : withIdList) {
            if (withId instanceof Subscription subscription) {
                subscriptionList.add(subscription);
            }
        }
        return subscriptionList;
    }

    public static List<Subscription> inactivateSubscriptions(Plan plan) {
        List<WithId> withIdList = Repository.loadAllObjectInDirectory("Subscription" + File.separator + plan.getName());
        List<Subscription> subscriptionList = new ArrayList<>();
        for (WithId withId : withIdList) {
            if (withId instanceof Subscription subscription) {
                subscription.setStatus(SubscriptionStatus.INACTIVE);
                subscription.setSuspensionDate(subscription.getNextChargeDate());
                subscription.setNextChargeDate(LocalDate.MIN);
                Repository.update(subscription, "Subscription" + File.separator + plan.getName());
                subscriptionList.add(subscription);
            }
        }
        return subscriptionList;
    }

    public static Plan getPlan(String name) {
        return (Plan) Repository.load("Plan", name);
    }

    public PlanStatus getStatus() {
        return status;
    }

    public void setStatus(PlanStatus status) {
        this.status = status;
    }
}
"""

"""

import java.time.LocalDate;

import baseDatos.Repository;
import gestorAplicacion.WithId;
import gestorAplicacion.customers.User;
import gestorAplicacion.gateways.Gateway;
import gestorAplicacion.gateways.GatewaysFactory;
import gestorAplicacion.transactions.Card;
import gestorAplicacion.transactions.Transaction;
import gestorAplicacion.transactions.TransactionStatus;

public class Subscription extends WithId {
    private static final long serialVersionUID = 2L;
    private transient User user;
    private transient Plan plan;
    private LocalDate nextChargeDate;
    private LocalDate startDate;
    private SubscriptionStatus status;
    private int numberOfCollectionAttempts = 0;
    private Card card;
    private LocalDate suspensionDate;

    public Subscription(User user, Plan plan) {
        super(createId(user.getEmail(), plan.getName()));
        this.user = user;
        this.plan = plan;
        this.startDate = LocalDate.now();
        this.status = SubscriptionStatus.INACTIVE;
        this.nextChargeDate = LocalDate.now();
        this.suspensionDate = LocalDate.MAX;
    }

    public Subscription(User user, Plan plan, LocalDate startDate) {
        this(user, plan);
        if (startDate.isAfter(LocalDate.now())) {
            this.startDate = startDate;
            this.nextChargeDate = startDate;
        }
    }

    public Subscription(User user, Plan plan, Card card) {
        this(user, plan);
        this.card = card;
    }

    public Subscription(User user, Plan plan, LocalDate startDate, Card card) {
        this(user, plan, startDate);
        this.card = card;
    }

    public Transaction processPayment(Transaction transaction) {
        GatewaysFactory.getGateway(this.user.getGateway()).pay(transaction);
        if(transaction.getStatus() == TransactionStatus.ACCEPTED && this.nextChargeDate.isAfter(LocalDate.now().plusDays(1))) {
            long remainingDays = this.nextChargeDate.toEpochDay() - LocalDate.now().toEpochDay();
            this.nextChargeDate = LocalDate.now().plusMonths(1).plusDays(remainingDays);
        }
        else if (transaction.getStatus() == TransactionStatus.ACCEPTED) {
            this.nextChargeDate = LocalDate.now().plusMonths(1);
            this.status = SubscriptionStatus.ACTIVE;
        } else if (this.numberOfCollectionAttempts < 3) {
            // update next charge date to tomorrow
            this.nextChargeDate = LocalDate.now().plusDays(1);
            this.status = SubscriptionStatus.PENDING;
            this.numberOfCollectionAttempts++;
        } else {
            this.status = SubscriptionStatus.CANCELLED;
        }
        Repository.update(this, "Subscription" + java.io.File.separator + this.plan.getName());
        return transaction;
    }

    public Gateway getGateway() {
        return this.user.getGateway();
    }

    public Transaction processPayment() {
        Transaction transaction = new Transaction(
            this.plan.getName(),
            this.user,
            this.plan.getPrice(),
            TransactionStatus.PENDING,
            this.getPaymentMethod()
        );

        return processPayment(transaction);
    }

    public boolean upsertPaymentMethod(Card card) {
        this.setPaymentMethod(card);
        Repository.update(this);

        Transaction transaction = new Transaction(
            this.plan.getName(),
            this.user,
            1,
            TransactionStatus.PENDING
        );
        processPayment(transaction);
        return transaction.getStatus() == TransactionStatus.ACCEPTED;
    }

    public User getUser() {
        return user;
    }

    public Card getPaymentMethod () {
        if(this.card == null) {
            return this.user.getCreditCards().get(0);
        }

        return this.card;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Plan getPlan() {
        return plan;
    }

    public void setPlan(Plan plan) {
        this.plan = plan;
    }

    public void setPaymentMethod(Card card) {
        this.card = card;
    }

    public LocalDate getNextChargeDate() {
        return nextChargeDate;
    }

    public SubscriptionStatus getStatus() {
        return status;
    }

    public void setStatus(SubscriptionStatus status) {
        this.status = status;
    }

    public LocalDate getStartDate() {
        return startDate;
    }

    public void setNextChargeDate(LocalDate nextChargeDate) {
        this.nextChargeDate = nextChargeDate;
    }

    public void setSuspensionDate(LocalDate date) {
        this.suspensionDate = date;
    }

    public LocalDate getSuspensionDate() {
        return this.suspensionDate;
    }
}
"""
class PlanStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
"""
package gestorAplicacion.plan;

public enum PlanStatus {
    ACTIVE,
    INACTIVE
}
"""
class SubscriptionStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"
"""
package gestorAplicacion.plan;

public enum SubscriptionStatus {
    ACTIVE,
    INACTIVE,
    CANCELLED,
    PENDING,
}
"""