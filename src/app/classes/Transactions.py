import WithId
import Customer
import Plan
import Gateways

class Transaction(WithId):
    def __init__(self, description, user, price):
        super().__init__(self.create_id(self.get_month_and_year(), user.get_email()))
        self.description = description
        self.price = price
        self.user_email = user.get_email()
        #self.gateway = user.get_gateway()
        #self.date = datetime.now()

    def __init__(self, description, user, price, status):
        self(description, user, price)
        self.status = status

    def __init__(self, description, user, price, status, card):
        self(description, user, price, status)
        self.payment_method = card

    def get_payment_method(self):
        return self.payment_method

    def set_payment_method(self, payment_method):
        self.payment_method = payment_method

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    def get_user_email(self):
        return self.user_email

    def get_gateway(self):
        return self.gateway

    def get_date(self):
        return self.date

    @staticmethod
    def get_month_and_year():
        return datetime.now().strftime("%m-%Y")

    @staticmethod
    def create_id(attribute1, attribute2):
        return WithId.create_id(attribute1, attribute2)
"""
package gestorAplicacion.transactions;

import java.time.LocalDate;
import java.util.Calendar;

import gestorAplicacion.WithId;
import gestorAplicacion.customers.User;
import gestorAplicacion.gateways.Gateway;

public class Transaction extends WithId {
    private Card paymentMethod;
    private  TransactionStatus status;
    private String description;
    private double price;
    private String userEmail;
    private Gateway gateway;
    private LocalDate date;

    private static String getMontAndYear() {
        return Calendar.getInstance().get(Calendar.MONTH) + "-" + Calendar.getInstance().get(Calendar.YEAR);
    }

    public Transaction(String description, User user, double price) {
        super(createId(getMontAndYear(), user.getEmail()));
        this.description = description;
        this.price = price;
        this.userEmail = user.getEmail();
        this.gateway = user.getGateway();
        this.date = LocalDate.now();
    }

    public Transaction(String description, User user, double price, TransactionStatus status) {
        this(description, user, price);
        this.userEmail = user.getEmail();
        this.gateway = user.getGateway();
        this.status = status;
    }

    public Transaction(
        String description,
        User user,
        double price,
        TransactionStatus status,
        Card card
    ) {
        this(description, user, price, status);
        this.paymentMethod = card;
    }

    public Card getPaymentMethod() {
        return paymentMethod;
    }

    public void setPaymentMethod(Card paymentMethod) {
        this.paymentMethod = paymentMethod;
    }

    public TransactionStatus getStatus() {
        return status;
    }

    public void setStatus(TransactionStatus status) {
        this.status = status;
    }

    public String getDescription() {
        return description;
    }

    public double getPrice() {
        return price;
    }

    public String getUserEmail() {
        return userEmail;
    }

    public Gateway getGateway() {
        return gateway;
    }

    public LocalDate getDate() {
        return date;
    }
}
"""
class Card(WithId):
    def __init__(self, last_four, due_date, franchise, token, gateway, card_owner):
        super().__init__(self.create_id(due_date, last_four))
        self.due_date = due_date
        self.last_four = last_four
        self.franchise = franchise
        self.token = token
        self.gateway = gateway
        self.card_owner = card_owner

    def get_due_date(self):
        return self.due_date

    def get_last_four(self):
        return self.last_four

    def get_franchise(self):
        return self.franchise

    def get_token(self):
        return self.token

    def delete(self):
        #self.gateway.delete_card(self)

    def get_card_owner(self):
        return self.card_owner
    """
    @staticmethod
    def get_franchise(number):
        if number.startswith("4"):
            return Franchise.VISA
        elif number.startswith("5"):
            return Franchise.MASTERCARD
        elif number.startswith("6"):
            return Franchise.DISCOVER
        else:
            return Franchise.UNKNOWN
    """
"""
package gestorAplicacion.transactions;

import gestorAplicacion.WithId;
import gestorAplicacion.customers.User;
import gestorAplicacion.gateways.Gateway;
import gestorAplicacion.gateways.GatewaysFactory;

public class Card extends WithId {
    private String dueDate;
    private String lastFour;
    private Franchise franchise;
    private final String TOKEN;
    private Gateway gateway;
    private transient User cardOwner;

    public Card(
        String lastFour,
        String dueDate,
        Franchise franchise,
        String token,
        Gateway gateway,
        User cardOwner
    ) {
        super(createId(dueDate, lastFour));
        this.dueDate = dueDate;
        this.lastFour = lastFour;
        this.franchise = franchise;
        this.TOKEN = token;
        this.gateway = gateway;
        this.cardOwner = cardOwner;
    }

    public String getExpirationDate() {
        return dueDate;
    }

    public String getLastFour() {
        return lastFour;
    }

    public Franchise getFranchise() {
        return franchise;
    }

    public String getTOKEN() {
        return TOKEN;
    }

    public void delete() {
        GatewaysFactory.getGateway(this.gateway).deleteCard(this);
    }

    public User getCardOwner() {
        return cardOwner;
    }

    public static Franchise getFranchise(String number) {
        if (number.startsWith("4")) {
            return Franchise.VISA;
        } else if (number.startsWith("5")) {
            return Franchise.MASTERCARD;
        } else if (number.startsWith("6")) {
            return Franchise.DISCOVER;
        } else {
            return Franchise.UNKNOWN;
        }
    }
}
"""
class Franchise(Enum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    AMERICAN_EXPRESS = "AMERICAN EXPRESS"
    DINERS_CLUB = "DINERS CLUB"
    DISCOVER = "DISCOVER"
    JCB = "JCB"
    UNIONPAY = "UNIONPAY"
    MAESTRO = "MAESTRO"
    VISA_ELECTRON = "VISA_ELECTRON"
    V_PAY = "V_PAY"
    MIR = "MIR"
    TROY = "TROY"
    UATP = "UATP"
    UNKNOWN = "UNKNOWN"

"""
package gestorAplicacion.transactions;

public enum Franchise {
    VISA,
    MASTERCARD,
    AMERICAN_EXPRESS,
    DINERS_CLUB,
    DISCOVER,
    JCB,
    UNIONPAY,
    MAESTRO,
    VISA_ELECTRON,
    V_PAY,
    MIR,
    TROY,
    UATP,
    UNKNOWN,
}
"""
class TransactionStatus(Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    REVERSED = "REVERSED"
"""
package gestorAplicacion.transactions;

public enum TransactionStatus {
    ACCEPTED,
    REJECTED,
    PENDING,
    CANCELLED,
    REVERSED,
}
"""