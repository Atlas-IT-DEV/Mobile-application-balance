import { Image, StyleSheet, Text, TouchableOpacity, View } from "react-native";

const FundCard = ({
  uri = "https://legacy.reactjs.org/logo-og.png",
  name = "Ремонт дома для пожилой пары",
  collect_sum = 30000,
  full_sum = 100000,
}) => {
  return (
    <View style={styles.container}>
      <Image
        source={{ uri: uri }}
        height={150}
        width={"100%"}
        style={styles.mainImage}
      />

      <View style={styles.mainInfo}>
        <Text style={styles.nameText}>{name}</Text>
        <View style={styles.progressBar}>
          <View
            style={[
              styles.progressFillBar,
              { width: `${(collect_sum / full_sum) * 100}%` },
            ]}
          />
        </View>
        <View style={styles.progressSum}>
          <Text style={styles.moneyText}>
            {collect_sum.toLocaleString("ru")} ₽
          </Text>
          <Text style={styles.moneyText}>
            {full_sum.toLocaleString("ru")} ₽
          </Text>
        </View>
        <View style={styles.buttonsView}>
          <TouchableOpacity style={[styles.button, styles.detailsButton]}>
            <Text style={styles.detailsText}>Подробнее</Text>
          </TouchableOpacity>
          <TouchableOpacity style={[styles.button, styles.helpButton]}>
            <Text style={styles.helpText}>Помочь</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: "rgba(255,255,255,1)",
    borderRadius: 20,
    shadowColor: "rgba(36, 27, 79, 0.2)",
    shadowOffset: {
      width: 3,
      height: 3,
    },
    shadowOpacity: 0.7,
    shadowRadius: 2,
  },
  mainImage: {
    objectFit: "cover",
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
  },
  mainInfo: {
    padding: 20,
    marginTop: 15,
  },
  nameText: {
    fontSize: 16,
    fontFamily: "IBMMedium",
    color: "rgba(52, 52, 52, 1)",
  },
  progressBar: {
    width: "100%",
    height: 5,
    marginTop: 15,
    backgroundColor: "rgba(70, 47, 181, 0.3)",
    borderRadius: 3,
    position: "relative",
  },
  progressFillBar: {
    backgroundColor: "rgba(22, 3, 111, 1)",
    position: "absolute",
    left: 0,
    top: 0,
    height: 5,
    borderRadius: 3,
  },
  progressSum: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 10,
  },
  moneyText: {
    color: "rgba(52, 52, 52, 1)",
    fontFamily: "IBMMedium",
  },
  buttonsView: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 15,
    gap: 5,
  },
  button: {
    width: "50%",
    alignItems: "center",
    justifyContent: "center",
    height: 35,
    borderRadius: 10,
  },
  detailsButton: {
    borderWidth: 1,
    borderColor: "rgba(22, 3, 111, 1)",
  },
  detailsText: {
    fontFamily: "IBMMedium",
    color: "rgba(22, 3, 111, 1)",
  },
  helpButton: {
    backgroundColor: "rgba(48, 31, 129, 1)",
  },
  helpText: {
    fontFamily: "IBMSemiBold",
    color: "white",
  },
});

export default FundCard;
