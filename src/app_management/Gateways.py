import WithId
import Customer
import Plan
import Transactions

class Credential(WithId):
    def __init__(self, public_key, private_key, gateway):
        super().__init__(gateway.get_name())
        self.public_key = public_key
        self.private_key = private_key
        self.gateway = gateway

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def get_gateway(self):
        return self.gateway
"""
package gestorAplicacion.gateways;

import gestorAplicacion.WithId;

public class Credential extends WithId {
    private final String PUBLIC_KEY;
    private final String PRIVATEKEY;
    private final Gateway GATEWAY;

    public Credential(String publicKey, String privateKey, Gateway gateway) {
        super(gateway.toString());
        this.PUBLIC_KEY = publicKey;
        this.PRIVATEKEY = privateKey;
        this.GATEWAY = gateway;
    }

    public String getPublicKey() {
        return PUBLIC_KEY;
    }

    public String getPrivateKey() {
        return PRIVATEKEY;
    }

    public Gateway getGateway() {
        return GATEWAY;
    }
}
"""
class GatewaysFactory:
    def __init__(self, gateway):
        self.gateways = {}
        self.gateway = gateway
        self.initialize_gateway()

    def __init__(self, gatewaysToAdd):
        self.gateways = {}
        self.iterate_and_add(gatewaysToAdd)

    def iterate_and_add(self, gatewaysToAdd):
        for gateway in gatewaysToAdd:
            self.gateways[gateway] = ProjectGateway()

    def get_gateway(self, gateway):
        return self.gateways.get(gateway)

    def initialize_gateway(self, gateway):
        if not self.gateways:
            self.gateways[gateway] = ProjectGateway()
        else:
            self.gateways[gateway] = ProjectGateway()

    def initialize_gateways(self, gatewaysAndCredentials):
        if not self.gateways:
            self.iterate_and_add(gatewaysAndCredentials)
        else:
            self.iterate_and_add(gatewaysAndCredentials)
"""
package gestorAplicacion.gateways;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;

public class GatewaysFactory {
    private static Map<Gateway, IGateway> gateways = new EnumMap<>(Gateway.class);

    private GatewaysFactory(Gateway gateway) {
        switch (gateway) {
            case OTHER:
                break;
            case PROJECT_GATEWAY:
                gateways.put(gateway, new ProjectGateway());
                break;
            default:
                break;
        }
    }

    private GatewaysFactory(List<Gateway> gatewaysToAdd) {
        iterateAndAdd(gatewaysToAdd);
    }

    private static void iterateAndAdd(List<Gateway> gatewaysToAdd) {
        for (Gateway gateway : gatewaysToAdd) {
            gateways.put(gateway, new ProjectGateway());
        }
    }

    public static IGateway getGateway(Gateway gateway) {
        return gateways.get(gateway);
    }

    public static void initializeGateway(Gateway gateway) {
        if (gateways.isEmpty()) {
            new GatewaysFactory(gateway);
        } else {
            GatewaysFactory.gateways.put(gateway, new ProjectGateway());
        }
    }

    public static void initializeGateways(List<Gateway> gatewaysAndCredentials) {
        if (gateways.isEmpty()) {
            new GatewaysFactory(gatewaysAndCredentials);
        } else {
            iterateAndAdd(gatewaysAndCredentials);
        }
    }
}
"""
class ProjectGateway(Authenticate, IGateway):
    def __init__(self):
        super().__init__(Gateway.PROJECT_GATEWAY)

    def pay(self, transaction):
        transaction.set_status(TransactionStatus.ACCEPTED)
        return transaction

    def authenticated(self):
        return self.AUTHENTICATION_TOKEN != None

    @staticmethod
    def generate_card_token(card_number, card_holder, expiration_date):
        value = card_number + card_holder + expiration_date
        token_builder = ""
        for i in range(len(value)):
            token_builder += str(ord(value[i]))
        return token_builder

    def add_credit_card(self, card_number, card_holder, expiration_date, cvv, user):
        if not self.validate(card_number, card_holder, expiration_date, cvv):
            return None
        card = Card(
            card_number[-4:],
            expiration_date,
            Card.get_franchise(card_number),
            self.generate_card_token(card_number, card_holder, expiration_date),
            Gateway.PROJECT_GATEWAY,
            user
        )
        Repository.save(card, "Card" + os.path.sep + user.get_id())
        return card

    def delete_card(self, card):
        return True
"""
package gestorAplicacion.gateways;

import java.io.File;

import baseDatos.Repository;
import gestorAplicacion.customers.User;
import gestorAplicacion.transactions.Card;
import gestorAplicacion.transactions.Transaction;
import gestorAplicacion.transactions.TransactionStatus;

public class ProjectGateway extends Authenticate implements IGateway {

    public ProjectGateway() {
        super(Gateway.PROJECT_GATEWAY);
    }

    public Transaction pay(Transaction transaction) {
        transaction.setStatus(TransactionStatus.ACCEPTED);
        return transaction;
    }

    public boolean authenticated() {
        return this.AUTHENTICATION_TOKEN != null;
    }

    private static String generateCardToken(String cardNumber, String cardHolder, String expirationDate) {
        // simulate encryption of the card number, card holder and expiration date to generate a token
        String value =  cardNumber  + cardHolder + expirationDate;
        StringBuilder tokenBuilder = new StringBuilder();
        for (int i = 0; i < value.length(); i++) {
            tokenBuilder.append((int) value.charAt(i));
        }
        return tokenBuilder.toString();
    }

    public Card addCreditCard(String cardNumber, String cardHolder, String expirationDate, String cvv, User user) {
        if (!validate(cardNumber, cardHolder, expirationDate, cvv)) {
            return null;
        }
        Card card = new Card(
            cardNumber.substring(cardNumber.length() - 4, cardNumber.length()),
            expirationDate,
            Card.getFranchise(cardNumber),
            generateCardToken(cardNumber, cardHolder, expirationDate), Gateway.PROJECT_GATEWAY,
            user
        );

        Repository.save(card, "Card" + File.separator + user.getId());

        return card;
    }

    public boolean deleteCard(Card card) {
        // delete card from the database
        return true;
    }
}
"""
class Authenticate:
    def __init__(self, gateway):
        #credential = Repository.load("Credential", gateway.get_name())
        self.AUTHENTICATION_TOKEN = credential.get_public_key() + credential.get_private_key()

    def get_authentication_token(self):
        return self.AUTHENTICATION_TOKEN
"""
package gestorAplicacion.gateways;

import baseDatos.Repository;

public abstract class Authenticate {
    protected final String AUTHENTICATION_TOKEN;

    protected Authenticate(Gateway gateway) {
        Credential credential = (Credential) Repository.load("Credential", gateway.toString());
        // simulate request to the gateway to authenticate
        this.AUTHENTICATION_TOKEN = credential.getPublicKey() + credential.getPrivateKey();
    }
    public String getAuthenticationToken(){
        return AUTHENTICATION_TOKEN;
    }
}
"""
#######################################################
"""
package gestorAplicacion.gateways;

import gestorAplicacion.customers.User;
import gestorAplicacion.transactions.Card;
import gestorAplicacion.transactions.Transaction;

public interface IGateway {
    Transaction pay(Transaction transaction);
    Card addCreditCard(String cardNumber, String cardHolder, String expirationDate, String cvv, User user);
    boolean authenticated();
    public boolean deleteCard(Card card);
    public default boolean validate(String cardNumber, String cardHolder, String expirationDate, String cvv) {
        return cardNumber.length() > 4
                && cardHolder.length() > 3
                && expirationDate.matches("\\d{2}/\\d{2}")
                && cvv.length() > 2 && cvv.length() < 5;
    }
}
"""
class Gateway(Enum):
    OTHER = "OTHER"
    PROJECT_GATEWAY = "PROJECT_GATEWAY"
""" 
package gestorAplicacion.gateways;

public enum Gateway {
    OTHER,
    PROJECT_GATEWAY,
}

"""